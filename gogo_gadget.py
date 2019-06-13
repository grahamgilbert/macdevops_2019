#!/usr/bin/python
from __future__ import print_function
import subprocess
import base64
import os


def get_output(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)
    rc = process.poll()
    return rc


def main():
    print(get_output(["terraform", "init"]))
    print(get_output(["terraform", "plan"]))
    print(get_output(["terraform", "apply", "-auto-approve"]))
    repo_url = get_output(["terraform", "output", "cloudfront_url"])
    munki_bucket = get_output(["terraform", "output", "munki_bucket_id"])
    username = get_output(["terraform", "output", "username"])
    password = get_output(["terraform", "output", "password"])
    pwd_string = "{}:{}".format(username, password)
    auth = "Authorization: Basic {}".format(base64.b64encode(pwd_string))

    print(
        get_output(
            [
                "/usr/local/bin/aws",
                "s3",
                "sync",
                "munki_repo/",
                "s3://" + munki_bucket,
                "--exclude",
                ".git/*",
                "--exclude",
                ".git*",
            ]
        )
    )

    if os.path.exists("basic_auth_lambda.zip"):
        os.remove("basic_auth_lambda.zip")

    profile = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>PayloadContent</key>
    <array>
      <dict>
        <key>PayloadContent</key>
        <dict>
          <key>ManagedInstalls</key>
          <dict>
            <key>Forced</key>
            <array>
              <dict>
                <key>mcx_preference_settings</key>
                <dict>
                  <key>AdditionalHttpHeaders</key>
                  <array>
                    <string>{}</string>
                  </array>
                  <key>SoftwareRepoURL</key>
                  <string>https://{}</string>
                </dict>
              </dict>
            </array>
          </dict>
        </dict>
        <key>PayloadEnabled</key>
        <true/>
        <key>PayloadIdentifier</key>
        <string>MCXToProfile.1dc15df4-d4c4-4b3a-b507-dd8f3b44f093.alacarte.customsettings.2beb4aeb-861b-4000-8c3a-d05117bf5ba7</string>
        <key>PayloadType</key>
        <string>com.apple.ManagedClient.preferences</string>
        <key>PayloadUUID</key>
        <string>7A4E85DA-930D-44E1-A18A-49E28A4D817D</string>
        <key>PayloadVersion</key>
        <integer>1</integer>
      </dict>
    </array>
    <key>PayloadDescription</key>
    <string>Included custom settings: ManagedInstalls</string>
    <key>PayloadDisplayName</key>
    <string>Settings for Munki</string>
    <key>PayloadIdentifier</key>
    <string>ManagedInstalls</string>
    <key>PayloadOrganization</key>
    <string>MacDevOps:YVR</string>
    <key>PayloadRemovalDisallowed</key>
    <true/>
    <key>PayloadScope</key>
    <string>System</string>
    <key>PayloadType</key>
    <string>Configuration</string>
    <key>PayloadUUID</key>
    <string>32B15C05-5ECC-4AD5-8A90-3AA2D25B022D</string>
    <key>PayloadVersion</key>
    <integer>1</integer>
  </dict>
</plist>
""".format(
        auth, repo_url
    )

    with open("ManagedInstalls.mobileconfig", "w") as filehandle:
        filehandle.write(profile)


if __name__ == "__main__":
    main()
