# Django ISO Manager

Django ISO Manager is a repository replication manager written in Python using the Django Framework.

This Django App manages an ISO repository for Operation Systems (OS) images like Windows or Linux. 

---

## Installation and usage

Clone repository

`$ git clone https://github.com/raph/django_iso_manager.git`

Change into the project's directory

`$ cd django_iso_manager/`

Install requirements

`$ pip install -r requirements.txt`

Make migrations

`$ python manage.py makemigrations`

Migrate

`$ python manage.py migrate`

Create admin user

`$ python manage.py createsuperuser`

Run the app

`$ python manage.py runserver`

Go to http://127.0.0.1:8000/admin and enter credentials you created earlier with `createsuperuser`

At this stage, it is possible to scan a folder with ISO images (ISOMANAGER > Auto-Update Targets > Add Auto-Update Target). This works better if all the images are already registered in the catalog (see [below](#Example json data for importing an ISO) for its format). Alternative, you can add individual ISO images in ISOMANAGER > Managed Items > Add Managed Item). In that case, you will have to create a Catalog Item for the ISO (Library Item -> '+').

### The app functionality includes:

- [x] Admin management console (django admin)
- [ ] Scan repository folder and auto-add ISOs
- [x] Import ISO images into a catalog using json
- [x] Export ISO catalog data in various formats (json, yaml, csv, html, xlsx, etc.)
- [ ] Verify SHA256 checksums of the existing images in the datastore
- [ ] Select how often to update the catalog data from datastore
- [x] Add ISO with custom name
- [ ] Filter Catalog items by OS version, version scheme, name, architecture, language
- [ ] Filter Managed images by OS version, version scheme, name, architecture, language
- [x] Select which ISOs are to be managed by the app (managed items)
- [x] Attach update rules for ISOs for managed items (LTS, Major ver, Minor ver)
- [x] Select priority for updating catalogs of ISOs
- [ ] Select download options: bittorrent download, remote library download(nfs, smb s3), remote share storage driver(nfs, smb, s3)
- [ ] Download all latest images from specific os family (or other conditions)
- [ ] Verify SHA256 checksum after download
- [ ] Select whether to keep or delete old version of an ISO after update
- [ ] Records of downloads (download_list) and deleted items (delete_list)
- [ ] Custom folder structure (default structure will require the standard Family/OS - Flavor/os.vanilla-1.0.1.iso)

### Example json data for importing an ISO:
```
            {
                "os_edition_type":"LINUX",
                "os_edition_name":"Ubuntu Server",
                "os_edition_version":"20.04.3",
                "os_edition_arch":"AMD64",
                "os_edition_language":"ENGLISH",
                "os_edition_version_scheme":"calver",
                "os_edition_description":"Ubuntu 20.04.3 LTS (Focal Fossa) Live Server amd64",
                "contributors":"John Doe, jo@email.com",
                "author":"Canonical",
                "private":"0",
                "sha256sum":"jlkjl",
                "sha256sum_gpg":"jkljlkj",
                "release_date":"2021-11-16 15:06:29",
                "description":"ubuntu iso item",
                "keywords":"linux, ubuntu, calver",
                "original_filename":"Ubuntu-20.04.3-live-server-amd64.iso",
                "last_update":"2021-11-16 15:06:47",
                "homepage_url":"ubuntu.org",
                "documentation_url":"ubuntu.org/documentation/",
                "download_urls":"{'k': 'v'}"
            }
```

## Developer Documentation

---

### Entity relation diagram
![ERD](./docs/images/erd.jpg?raw=true "ERD")


### Creating an update target flowchart
![Create update target flowchart](./docs/images/create-update-target-flowchart.jpg?raw=true "Create update target steps")

### Updating managed items state diagram
![Updating managed items](./docs/images/update-target-state-diagram.jpg?raw=true "Updating managed item")
