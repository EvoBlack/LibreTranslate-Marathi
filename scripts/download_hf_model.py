from huggingface_hub import snapshot_download
import sys

repo_id = 'HariSekhar/Eng_Marathi_translation'
local_dir = './eng_marathi_translation'

print('Downloading', repo_id, 'to', local_dir)
snapshot_download(repo_id=repo_id, local_dir=local_dir)
print('Downloaded to', local_dir)
