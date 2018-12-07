from django.db import models


# Create your models here.


class ClassList(models.Model):
    course = models.CharField("课程名称", max_length=64)
    semester = models.IntegerField("学期")
    memo = models.CharField('说明', blank=True, null=True, max_length=100)

    class Meta:
        verbose_name = "班级列表"


class SurveyItem(models.Model):
    name = models.CharField("调查问题", max_length=255)
    date = models.DateField(auto_now_add=True)
    answer_type_choices = (('single', "单选"), ('suggestion', "建议"))
    answer_type = models.CharField("问题类型", choices=answer_type_choices, default='score', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '调查问卷问题列表'
        verbose_name_plural = "调查问卷问题列表"


class SurveyChoices(models.Model):
    question = models.ForeignKey("SurveyItem", verbose_name='问题', related_name='answers', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='答案内容', max_length=256, )
    points = models.IntegerField(verbose_name='分值', )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '问卷调查候选答案'
        verbose_name_plural = '问卷调查候选答案'


class SurveyCode(models.Model):
    """
    问卷唯一码
    """
    survey = models.ForeignKey("Survey", on_delete=models.CASCADE)
    unique_code = models.CharField(max_length=32, unique=True)
    used = models.BooleanField(default=False, verbose_name="使用状态")
    used_time = models.DateTimeField(blank=True, null=True, verbose_name='使用时间')
    date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")


class Survey(models.Model):
    name = models.CharField("调查问卷名称", max_length=128, unique=True)
    questions = models.ManyToManyField("SurveyItem", verbose_name="选择要调查的问题列表")
    by_class = models.ForeignKey("ClassList", verbose_name="问卷调查班级", on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True, verbose_name="第几次问卷调查")
    date = models.DateTimeField(auto_now_add=True, verbose_name="问卷创建日期")
    quantity = models.PositiveIntegerField("数量", default=1, help_text='生成唯一码的数量')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'调查问卷'
        verbose_name_plural = u"调查问卷"

        ordering = ["-date", ]

    @staticmethod
    def _get_random_string():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        while True:
            if not SurveyCode.objects.filter(unique_code=code).exists():
                return code

    def save(self, *args, **kwargs):
        """
        调查问卷记录
        """
        super(Survey, self).save(*args, **kwargs)
        bulk_list = []

        for item in range(self.quantity):
            code = self._get_random_string()
            bulk_list.append(SurveyCode(survey=self, unique_code=code))

        SurveyCode.objects.bulk_create(bulk_list)


class SurveyRecord(models.Model):
    survey = models.ForeignKey("Survey", verbose_name="问卷", on_delete=models.CASCADE)
    survey_item = models.ForeignKey("SurveyItem", verbose_name="调查项", on_delete=models.CASCADE)
    score = models.IntegerField("评分", help_text="打分为0至10,0为非常不满意,10为非常满意,请自行斟酌", blank=True, null=True)
    suggestion = models.TextField("建议", max_length=1024, blank=True, null=True)
    single = models.ForeignKey("SurveyChoices", verbose_name='单选', blank=True, null=True, on_delete=models.CASCADE)
    survey_code = models.ForeignKey("SurveyCode", verbose_name="唯一码", blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name=u"答题日期")

    class Meta:
        verbose_name = "问卷记录"
        verbose_name_plural = "问卷记录"
