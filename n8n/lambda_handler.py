import json
import urllib3
import os
from datetime import datetime

def lambda_handler(event, context):
    try:
        print("=== LAMBDA STARTED ===")
        print(f"Event type: {type(event)}")
        
        # The event IS the GitHub payload (not wrapped in 'body')
        # API Gateway is passing the JSON directly to Lambda
        if isinstance(event, dict) and 'repository' in event:
            print("✅ Direct GitHub payload detected")
            payload = event
        elif isinstance(event, dict) and 'body' in event:
            print("✅ Proxy integration format detected")
            body = event.get('body', '')
            if isinstance(body, str):
                payload = json.loads(body)
            else:
                payload = body
        else:
            print(f"❌ Unexpected event format: {type(event)}")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unexpected event format'})
            }
        
        print(f"✅ Processing GitHub webhook for repository: {payload.get('repository', {}).get('name', 'unknown')}")
        
        # Extract commit information
        head_commit = payload.get('head_commit', {})
        repository = payload.get('repository', {})
        pusher = payload.get('pusher', {})
        
        # Extract changed files from commits
        all_changed_files = []
        snowflake_files = []
        
        for commit in payload.get('commits', []):
            # Get all file changes
            added = commit.get('added', [])
            modified = commit.get('modified', [])
            removed = commit.get('removed', [])
            
            all_changed_files.extend(added)
            all_changed_files.extend(modified)
            all_changed_files.extend(removed)
            
            # Filter for SQL/YAML files
            for file_path in (added + modified + removed):
                if file_path.endswith(('.sql', '.yaml', '.yml')):
                    snowflake_files.append(file_path)
        
        # Remove duplicates while preserving order
        snowflake_files = list(dict.fromkeys(snowflake_files))
        all_changed_files = list(dict.fromkeys(all_changed_files))
        
        # Build processed data for n8n
        processed_data = {
            'repository_name': repository.get('name', 'unknown'),
            'repository_full_name': repository.get('full_name', ''),
            'branch': payload.get('ref', 'refs/heads/main').split('/')[-1],
            'commit_id': head_commit.get('id', ''),
            'commit_message': head_commit.get('message', ''),
            'pusher': pusher.get('name', 'unknown'),
            'timestamp': datetime.now().isoformat(),
            
            # File information
            'snowflake_files': snowflake_files,
            'all_changed_files': all_changed_files,
            'total_files': len(all_changed_files),
            'total_sql_files': len(snowflake_files),
            
            # Deployment decision
            'requires_deployment': len(snowflake_files) > 0,
            
            # Target configuration
            'target_database': 'AIX_SHARED_DB',
            'target_schema': 'PUBLIC'
        }
        
        print(f"=== PROCESSING SUMMARY ===")
        print(f"Repository: {processed_data['repository_name']}")
        print(f"Commit: {processed_data['commit_id'][:8]}...")
        print(f"Total files changed: {processed_data['total_files']}")
        print(f"SQL files: {processed_data['snowflake_files']}")
        print(f"Requires deployment: {processed_data['requires_deployment']}")
        
        # Send to n8n
        n8n_url = os.environ.get('N8N_WEBHOOK_URL')
        if n8n_url:
            http = urllib3.PoolManager()
            
            print("=== SENDING TO N8N ===")
            response = http.request(
                'POST',
                n8n_url,
                body=json.dumps(processed_data),
                headers={
                    'Content-Type': 'application/json',
                    'Content-Length': str(len(json.dumps(processed_data)))
                }
            )
            print(json.dumps(processed_data))
            print(f"n8n response status: {response.status}")
            if response.status == 200:
                print("✅ Successfully sent to n8n")
            else:
                print(f"❌ n8n error: {response.data.decode('utf-8')}")
        else:
            print("❌ N8N_WEBHOOK_URL not configured")
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'GitHub webhook processed successfully',
                'files_processed': len(snowflake_files),
                'deployment_required': processed_data['requires_deployment']
            })
        }
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
