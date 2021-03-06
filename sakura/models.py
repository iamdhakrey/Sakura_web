from asgiref.sync import sync_to_async
from django.db import models

# Create your models here.


class ImagesModel(models.Model):
    image1 = models.ImageField(verbose_name="image1",
                               upload_to='welcome_images/',
                               width_field=1920,
                               height_field=872)
    image2 = models.ImageField(verbose_name="image2",
                               upload_to='welcome_images/',
                               width_field=1920,
                               height_field=872)
    image3 = models.ImageField(verbose_name="image3",
                               upload_to='welcome_images/',
                               width_field=1920,
                               height_field=872)


class WelcomeData(models.Model):

    server_id = models.BigIntegerField(primary_key=True)
    server_name = models.CharField(verbose_name="server_name", max_length=100)

    server_active = models.BooleanField(default=True)
    welcome_enable = models.BooleanField(default=False)
    self_role = models.BigIntegerField(null=True)
    welcome_channel = models.BigIntegerField(null=True)
    welcome_msg = models.CharField(max_length=3000)
    update_by = models.BigIntegerField(null=True)
    last_update = models.DateTimeField(null=True, auto_now=True)

    image1 = models.ImageField(null=True,
                               verbose_name="image1",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image2 = models.ImageField(null=True,
                               verbose_name="image2",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image3 = models.ImageField(null=True,
                               verbose_name="image3",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image4 = models.ImageField(null=True,
                               verbose_name="image4",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")
    image5 = models.ImageField(null=True,
                               verbose_name="image5",
                               upload_to='welcome_images/',
                               width_field="img_width",
                               height_field="img_height")

    img_width = models.PositiveIntegerField(default=1920)
    img_height = models.PositiveIntegerField(default=872)

    def who_updated(self):
        if self.update_by is not None:
            return '<@' + str(self.update_by) + '>'

    def mention_welcome_channel(self):
        if self.welcome_channel is not None:
            return '<#' + str(self.welcome_channel) + '>'
        else:
            return None

    def save(self, *args, **kwargs):
        super(WelcomeData, self).save(*args, **kwargs)


class Server(models.Model):
    server_id = models.BigIntegerField(verbose_name="Guild ID",
                                       primary_key=True)
    server_name = models.CharField(verbose_name="Guild Name", max_length=100)
    avatar = models.CharField(null=True, max_length=50)
    admin = models.CharField(null=True, max_length=100)
    owner = models.BigIntegerField(null=True)
    admin_role = models.CharField(null=True, max_length=100)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField("User")

    def __str__(self) -> str:
        """GUILD"""
        return '{0} ({1})'.format(self.server_name, self.server_id)

    def member_count(self):
        return self.members.count()

    class Meta():
        verbose_name = "Guild"

    objects = models.Manager()


class User(models.Model):
    member_id = models.BigIntegerField(verbose_name="Discord ID",
                                       primary_key=True)
    discord_tag = models.CharField(verbose_name="Member Name", max_length=50)

    @property
    def mention(self):
        return "<@" + str(self.member_id) + ">"

    @sync_to_async
    def join_server(self, server):
        if not server.member.filter(id=self.member_id).exists():
            server.member.add(self)

    def __str__(self) -> str:
        return self.discord_tag

    objects = models.Manager()


class SelfRole(models.Model):
    title = models.CharField(verbose_name="title", max_length=100, null=True)
    server = models.BigIntegerField(verbose_name="server id")
    message_id = models.BigIntegerField(verbose_name="message_id", unique=True)
    reaction = models.CharField(verbose_name="reaction", max_length=1000)
    max_role = models.IntegerField(verbose_name="max_role")
    channel_id = models.BigIntegerField(null=True)
    create_date = models.DateTimeField(verbose_name="create_date",
                                       auto_now_add=True)
    last_update = models.DateTimeField(null=True, auto_now=True)
    update_by = models.BigIntegerField(null=True)
    created_by = models.CharField(null=True, max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    def who_updated(self):
        if self.update_by is not None:
            return '<@' + str(self.update_by) + '>'


class HelpCmd(models.Model):
    category = models.CharField(verbose_name="category", max_length=100)
    cmd = models.CharField(verbose_name="cmd", max_length=100)
    brief = models.CharField(verbose_name="brief", max_length=100)
    description = models.CharField(verbose_name="description", max_length=1000)
    usage = models.CharField(verbose_name="usage", max_length=1000)
    alias = models.CharField(verbose_name="alias", max_length=1000)
