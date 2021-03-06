from django.db import models
from django.contrib.auth.models import User
from public.models import CommonInfo
from envx.models import Env
from appinput.models import App

# Create your models here.

IS_INC_TOT_CHOICES = (
    ('TOT', r'全量部署'),
    ('INC', r'增量部署'),
)

DEPLOY_TYPE_CHOICES = (
    ('deployall', r'发布所有'),
    ('deploypkg', r'发布程序'),
    ('deploycfg', r'发布配置'),
    ('rollback', r'回滚'),
)


class DeployStatus(CommonInfo):
    memo = models.CharField(max_length=1024,
                            blank=True,
                            verbose_name='备注')

    class Meta:
        db_table = 'deploy_status'


class DeployPool(CommonInfo):
    name = models.CharField(max_length=100,
                            blank=True,
                            null=True,
                            verbose_name='发布单编号')
    description = models.CharField(max_length=1024,
                                   blank=True,
                                   null=True,
                                   verbose_name='描述')
    app_name = models.ForeignKey(App,
                                 null=True,
                                 related_name='deploy_app_name',
                                 on_delete=models.CASCADE,
                                 verbose_name='APP应用')
    deploy_no = models.IntegerField(blank=True,
                                    null=True,
                                    default=0)
    branch_build = models.CharField(max_length=255,
                                    blank=True,
                                    null=True)
    jenkins_number = models.CharField(max_length=255,
                                      blank=True,
                                      null=True)
    code_number = models.CharField(max_length=255,
                                   blank=True,
                                   null=True)
    is_inc_tot = models.CharField(max_length=255,
                                  choices=IS_INC_TOT_CHOICES,
                                  blank=True,
                                  null=True,
                                  verbose_name='全量或增量部署')
    deploy_type = models.CharField(max_length=255,
                                   choices=DEPLOY_TYPE_CHOICES,
                                   blank=True,
                                   null=True,
                                   verbose_name='发布程序或配置')
    is_build = models.BooleanField(default=None,
                                   blank=True,
                                   null=True,
                                   verbose_name='软件是否编译成功')
    create_user = models.ForeignKey(User,
                                    null=True,
                                    related_name='create_user',
                                    on_delete=models.CASCADE,
                                    verbose_name='创建用户')
    nginx_url = models.URLField(default=None,
                                blank=True,
                                null=True,
                                verbose_name='软件包服务器URL')
    env_name = models.ForeignKey(Env,
                                 blank=True,
                                 null=True,
                                 related_name='deploy_env_name',
                                 on_delete=models.CASCADE,
                                 verbose_name='环境')
    deploy_status = models.ForeignKey(DeployStatus,
                                      blank=True,
                                      null=True,
                                      related_name='deploy_status',
                                      on_delete=models.CASCADE,
                                      verbose_name='发布单状态')

    class Meta:
        db_table = 'deploy_pool'


class History(CommonInfo):
    user = models.ForeignKey(User, blank=True, null=True,
                             related_name='history_user',
                             on_delete=models.CASCADE,
                             verbose_name='用户')
    app_name = models.ForeignKey(App, blank=True, null=True,
                                 related_name='history_app',
                                 on_delete=models.CASCADE,
                                 verbose_name='APP应用')
    env_name = models.ForeignKey(Env, blank=True, null=True,
                                 related_name='history_env',
                                 on_delete=models.CASCADE,
                                 verbose_name='环境')
    deploy_name = models.ForeignKey(DeployPool, blank=True, null=True,
                                    related_name='history_deploy',
                                    on_delete=models.CASCADE,
                                    verbose_name='发布单')
    do_type = models.CharField(max_length=32, blank=True, null=True,
                               verbose_name='操作类型')
    content = models.CharField(max_length=1024, blank=True, null=True,
                               verbose_name='操作内容')

    class Meta:
        db_table = 'history'
