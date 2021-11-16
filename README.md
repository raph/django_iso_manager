# Django ISO Manager

Django ISO Manager is a repository replication manager written in Python using the Django Framework.

This Django App manages an ISO repository for Operation Systems (OS) images like Windows or Linux.

---

## Infrastructure and requirements:

- AWS Elastic Beanstalk
- Codebuild
- Autoscaling groups
- Amazon Linux AMI

First, setup your development environment on AWS using the Elastic beanstalk service
the app should use codebuild, autoscaling groups and amazon linux

### The app function includes:

- Download once
- Download and update minor version
- Scan repository folder and auto-add ISO's
- *(optional) add iso with custom name*
- *(optional) include the iso checksum in the json as an optional field*

The App should start with:
- A list of existing  ISO files
- A JSON file representing the downloaded ISO files with the following data:
    - Family
    - Name
    - Flavor
    - Major version
    - Minor version
    - Patch version

### Example:
```
Family: Linux
Name: Ubuntu
Flavor: Server
major version: 20
minor version: 04
patch version: 2
```


From an Admin panel built using Django, the User should be able to:
- [ ] View the currently downloaded ISO files by family names, flavors and versions (Windows 10, Linux Ubuntu, etc.)
- [ ] Select which ISO files to update
- [ ]  Select which OS to download
- [ ]  Select which flavor of the OS to download
- [ ]  Select to which major version of the OS to update (precise version or `latest`)
- [ ]  Select to which minor version of the OS to update (precise version or `latest`)
- [ ]  Select to which patch version of the OS to update (precise version or `latest`)
-
** Latest update chain only works from right to left example:
** You cannot have latest major version and precise minor or patch version
** You cannot latest minor version and precise patch version
- Select how often to pull the new json file from the server
- Launch the update of the selected ISO files. This step should:
    - update the JSON file containing the list of downloaded ISO files (*optional, check when the file has last been updated, don't update if the json is less than 1 hour old)
    - download the desired ISO file(s)
    - delete the old ISO file(s) (*be careful not to delete ISO's that might be the 'best version' in two objects in the app!)



add feature: : bittorrent download, remote library download(nfs, smb s3), remote share storage driver(nfs, smb, s3)
add feature: custom folder structure (default structure will require the standard Family/OS - Flavor/os.vanilla-1.0.1.iso
add feature:  download all latest from specific os family (or other conditions)
add feature: add iso to catalog (form or json)
add feature: import iso from folder