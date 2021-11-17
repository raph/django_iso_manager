from unittest import mock
from django.test import TestCase
from django.contrib.auth import get_user_model

from isomanager.models import Datastore, ManagedItem, CatalogItem, RemoteCatalog

class TestIsoManager(TestCase):
    #TODO test DataStore.scan() (problem: scans location with glob)
    #TODO test UpdateTarget (problem: recurrence field)
    #TODO test if RemoteCatalog creation also creates cat items
    #TODO test admin: DatastoreAdmin.response_change (scan)
    #TODO test admin: RemoteCatalogAdmin.response_change (populate_cat_items)
    #TODO test utils: hash()

    def setUp(self):
        self.user_staff = get_user_model().objects.create_user(
            username='a',
            email='staff@a.com',
            password='testpass123',
            is_staff=True
        )

        self.js_cat = [
            {
                "id":1,
                "created_time":"2021-11-16 15:06:47",
                "updated_time":"2021-11-16 15:06:47",
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
                "original_filename":"buntu-20.04.3-live-server-amd64.iso",
                "last_update":"2021-11-16 15:06:47",
                "homepage_url":"ubuntu.org",
                "documentation_url":"ubuntu.org/documentation/",
                "download_urls":"{'k': 'v'}"
            }
        ]

    def test_create_datastore(self):
        self.client.login(username='a', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        data_store = Datastore.objects.create(
            datastore_type='PATH',
            location='some.location/path',
            auth_type='USER',
            username='a',
            password='bbb',
            readonly=False,
            last_scan='2021-11-16 15:06:29'
        )

        self.assertIsInstance(data_store, Datastore)
        self.assertEqual(data_store.__str__(), f'{data_store.datastore_type} - {data_store.location}')
        self.assertEqual(data_store.datastore_type, 'PATH')
        self.assertEqual(data_store.location, 'some.location/path')
        self.assertEqual(data_store.auth_type, 'USER')
        self.assertEqual(data_store.username, 'a')
        self.assertEqual(data_store.password, 'bbb')
        self.assertEqual(data_store.readonly, False)
        self.assertEqual(data_store.last_scan, '2021-11-16 15:06:29')

        return data_store

    def test_datastore_scan_method(self):
        pass


    def test_create_catalog_item(self):
        self.client.login(username='a', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        cat_item = CatalogItem.objects.create(
            os_edition_type='LINUX',
            os_edition_name='Ubuntu Server',
            os_edition_version='20.04.3',
            os_edition_arch='AMD64',
            os_edition_language='ENGLISH',
            os_edition_version_scheme='calver',
            os_edition_description='Ubuntu 20.04.3 LTS (Focal Fossa) Live Server amd64',
            contributors='John Doe, jo@email.com',
            author='Canonical',
            private=False,
            sha256sum='jlkjl',
            sha256sum_gpg='jkljlkj',
            release_date='2021-11-16 15:06:29',
            description='ubuntu iso item',
            keywords='linux, ubuntu, calver',
            original_filename='buntu-20.04.3-live-server-amd64.iso',
            last_update='2021-11-16 15:06:47',
            homepage_url='ubuntu.org',
            documentation_url='ubuntu.org/documentation/',
            download_urls={'k': 'v'},
        )

        self.assertIsInstance(cat_item, CatalogItem)
        self.assertEqual(cat_item.__str__(), f'{cat_item.os_edition_name} {cat_item.author}')
        self.assertEqual(cat_item.os_edition_type, 'LINUX')
        self.assertEqual(cat_item.os_edition_name, 'Ubuntu Server')
        self.assertEqual(cat_item.os_edition_version, '20.04.3')
        self.assertEqual(cat_item.os_edition_arch, 'AMD64')
        self.assertEqual(cat_item.os_edition_language, 'ENGLISH')
        self.assertEqual(cat_item.os_edition_version_scheme, 'calver')
        self.assertEqual(cat_item.os_edition_description, 'Ubuntu 20.04.3 LTS (Focal Fossa) Live Server amd64')
        self.assertEqual(cat_item.contributors, 'John Doe, jo@email.com')
        self.assertEqual(cat_item.author, 'Canonical')
        self.assertEqual(cat_item.private, False)
        self.assertEqual(cat_item.sha256sum, 'jlkjl')
        self.assertEqual(cat_item.sha256sum_gpg, 'jkljlkj')
        self.assertEqual(cat_item.release_date, '2021-11-16 15:06:29')
        self.assertEqual(cat_item.description, 'ubuntu iso item')
        self.assertEqual(cat_item.keywords, 'linux, ubuntu, calver')
        self.assertEqual(cat_item.original_filename, 'buntu-20.04.3-live-server-amd64.iso')
        self.assertEqual(cat_item.homepage_url, 'ubuntu.org')
        self.assertEqual(cat_item.documentation_url, 'ubuntu.org/documentation/')
        self.assertEqual(cat_item.download_urls, {'k': 'v'})

        return cat_item

    def test_create_managed_item(self):
        self.client.login(username='a', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        data_store = self.test_create_datastore()
        cat_item = self.test_create_catalog_item()
        man_item = ManagedItem.objects.create(
            full_path='some/path/to.iso',
            datastore=data_store,
            sha256sum='1234adsf',
            library_item=cat_item
        )

        self.assertIsInstance(cat_item, CatalogItem)
        self.assertEqual(man_item.__str__(), f'({man_item.sha256sum}) {man_item.full_path}')
        self.assertEqual(man_item.full_path, 'some/path/to.iso')
        self.assertEqual(man_item.datastore, data_store)
        self.assertEqual(man_item.library_item, cat_item)

        return man_item

    def test_create_remote_calalog(self):
        self.client.login(username='a', password='testpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        rem_cat = RemoteCatalog.objects.create(
            catalog_name='RemCat',
            json_catalog=self.js_cat,
            version='1.2',
            remote_url='aaaa.com',
            auto_update=True,
            priority='1',
        )

        self.assertIsInstance(rem_cat, RemoteCatalog)
        self.assertEqual(rem_cat.__str__(), f'{rem_cat.catalog_name}')
        self.assertEqual(rem_cat.catalog_name, 'RemCat')
        self.assertEqual(rem_cat.json_catalog, self.js_cat)
        self.assertEqual(rem_cat.version, '1.2')
        self.assertEqual(rem_cat.remote_url, 'aaaa.com')
        self.assertEqual(rem_cat.auto_update, True)
        self.assertEqual(rem_cat.priority, '1')

    def tearDown(self):
        self.user_staff.delete()





