# awsume-onepassword

An Awsume plugin to add support for storing AWS access keys and MFA data in 1Password

## Config

1. Ensure the 1Password CLI is installed and enabled in your desktop client
2. Create an item in 1Password with the following fields:
   * `one-time password`
   * `access key id`
   * `secret access key`
   * `mfa serial` 
3. Add the following to the awsume config:
    ```yaml
    onepassword:
      vault: Your Vault Name
      item: Your Item Name
    ```
