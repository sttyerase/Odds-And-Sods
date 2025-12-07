import dropbox
APP_KEY = ''
APP_SECRET = ''
REFRESH_TOKEN = ''

## OBTAIN DROPBOX CONNECTION
dbx = dropbox.Dropbox(
    app_key=APP_KEY,
    app_secret=APP_SECRET,
    oauth2_refresh_token=REFRESH_TOKEN
)

result = dbx.users_get_current_account()
print('ACCOUNT:\n', result)
root_namespace_id = dbx.users_get_current_account().root_info.root_namespace_id
print('ROOT_NAMESPACE:\n', root_namespace_id)
dbx = dbx.with_path_root(dropbox.common.PathRoot.root(root_namespace_id))
result = dbx.files_list_folder('')
print('LIST FOLDER:\n',result)
