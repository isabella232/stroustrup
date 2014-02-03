# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client_Story_Record'
        db.create_table(u'book_library_client_story_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['book_library.Book'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('book_taken', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('book_returned', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'book_library', ['Client_Story_Record'])

        # Adding model 'Author'
        db.create_table(u'book_library_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'book_library', ['Author'])

        # Adding model 'Book_Rating'
        db.create_table(u'book_library_book_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_owner', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='rating', blank=True, to=orm['auth.User'])),
            ('user_rating', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('common_rating', self.gf('django.db.models.fields.FloatField')(default=0, blank=True)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal(u'book_library', ['Book_Rating'])

        # Adding model 'Book_Comment'
        db.create_table(u'book_library_book_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sent_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='comment', blank=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'book_library', ['Book_Comment'])

        # Adding model 'Book'
        db.create_table(u'book_library_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('busy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('e_version_exists', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paperback_version_exists', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')(default='No description available.', max_length=255)),
            ('picture', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'book_library', ['Book'])

        # Adding M2M table for field authors on 'Book'
        m2m_table_name = db.shorten_name(u'book_library_book_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'book_library.book'], null=False)),
            ('author', models.ForeignKey(orm[u'book_library.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'author_id'])

        # Adding M2M table for field tags on 'Book'
        m2m_table_name = db.shorten_name(u'book_library_book_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'book_library.book'], null=False)),
            ('book_tag', models.ForeignKey(orm[u'book_library.book_tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'book_tag_id'])

        # Adding M2M table for field book_rating on 'Book'
        m2m_table_name = db.shorten_name(u'book_library_book_book_rating')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'book_library.book'], null=False)),
            ('book_rating', models.ForeignKey(orm[u'book_library.book_rating'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'book_rating_id'])

        # Adding M2M table for field comments on 'Book'
        m2m_table_name = db.shorten_name(u'book_library_book_comments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm[u'book_library.book'], null=False)),
            ('book_comment', models.ForeignKey(orm[u'book_library.book_comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'book_comment_id'])

        # Adding model 'Book_Tag'
        db.create_table(u'book_library_book_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'book_library', ['Book_Tag'])

        # Adding model 'Book_Request'
        db.create_table(u'book_library_book_request', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null='')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('vote', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'book_library', ['Book_Request'])

        # Adding M2M table for field users on 'Book_Request'
        m2m_table_name = db.shorten_name(u'book_library_book_request_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book_request', models.ForeignKey(orm[u'book_library.book_request'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_request_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Client_Story_Record'
        db.delete_table(u'book_library_client_story_record')

        # Deleting model 'Author'
        db.delete_table(u'book_library_author')

        # Deleting model 'Book_Rating'
        db.delete_table(u'book_library_book_rating')

        # Deleting model 'Book_Comment'
        db.delete_table(u'book_library_book_comment')

        # Deleting model 'Book'
        db.delete_table(u'book_library_book')

        # Removing M2M table for field authors on 'Book'
        db.delete_table(db.shorten_name(u'book_library_book_authors'))

        # Removing M2M table for field tags on 'Book'
        db.delete_table(db.shorten_name(u'book_library_book_tags'))

        # Removing M2M table for field book_rating on 'Book'
        db.delete_table(db.shorten_name(u'book_library_book_book_rating'))

        # Removing M2M table for field comments on 'Book'
        db.delete_table(db.shorten_name(u'book_library_book_comments'))

        # Deleting model 'Book_Tag'
        db.delete_table(u'book_library_book_tag')

        # Deleting model 'Book_Request'
        db.delete_table(u'book_library_book_request')

        # Removing M2M table for field users on 'Book_Request'
        db.delete_table(db.shorten_name(u'book_library_book_request_users'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'book_library.author': {
            'Meta': {'object_name': 'Author'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'book_library.book': {
            'Meta': {'ordering': "['title']", 'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'to': u"orm['book_library.Author']"}),
            'book_rating': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': u"orm['book_library.Book_Rating']", 'null': 'None', 'symmetrical': 'False', 'blank': 'True'}),
            'busy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'books'", 'blank': 'True', 'symmetrical': 'False', 'to': u"orm['book_library.Book_Comment']"}),
            'description': ('django.db.models.fields.TextField', [], {'default': "'No description available.'", 'max_length': '255'}),
            'e_version_exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'paperback_version_exists': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'blank': 'True', 'to': u"orm['book_library.Book_Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'books'", 'blank': 'True', 'through': u"orm['book_library.Client_Story_Record']", 'to': u"orm['auth.User']"})
        },
        u'book_library.book_comment': {
            'Meta': {'object_name': 'Book_Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'comment'", 'blank': 'True', 'to': u"orm['auth.User']"})
        },
        u'book_library.book_rating': {
            'Meta': {'object_name': 'Book_Rating'},
            'common_rating': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_owner': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'rating'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'user_rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'})
        },
        u'book_library.book_request': {
            'Meta': {'object_name': 'Book_Request'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': "''"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['auth.User']", 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'request'", 'blank': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'book_library.book_tag': {
            'Meta': {'object_name': 'Book_Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'book_library.client_story_record': {
            'Meta': {'object_name': 'Client_Story_Record'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['book_library.Book']"}),
            'book_returned': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'book_taken': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['book_library']