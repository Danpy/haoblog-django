# coding=utf8

from django import forms

class CommentForm(forms.Form):
    author = forms.CharField(max_length=30, help_text='默认为‘None’', label='ID:', initial='你的大名 :)')
    email = forms.CharField(max_length=75, help_text='请相信我不会公开:)', label='Eamil:', initial='haoglog.admin@gmail.com')
    site_url = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size': 60}), help_text='blog/github/weblog', label='Site:', initial='http://google.com')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}), label='', initial='add a comment')
    entry_id = forms.CharField(widget=forms.HiddenInput())

    def __unicode__(self):
        return u'%s %s %s %s %s' % (
                self.author,
                self.email,
                self.site_url,
                self.entry_id,
                self.content
        )
