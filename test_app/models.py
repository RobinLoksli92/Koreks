from django.db import models


class Question(models.Model):
    LEVELS = [
        (1, 'Легкий'),
        (2, 'Средний'),
        (3, 'Сложный'),
        (4, 'Высший разум')
    ]
    ANSWERS = [
        ('Yes', 'Да'),
        ('No', 'Нет')
    ]

    text = models.CharField('Вопрос', max_length=255, blank=True, unique=True)
    answer = models.TextField('Ответ', choices=ANSWERS, null=True)
    level = models.PositiveBigIntegerField('уровень сложности', choices=LEVELS, blank=True, null=True)
    test = models.ForeignKey('Test', on_delete=models.CASCADE, blank=True, null=True)          #Точка расширения: ManyToManyField, для использования вопросов в разных тестах.

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
    
    def __str__(self):
        return self.text


class Test(models.Model):
    # Можно увеличить кол-во полей, дать названия тестам, добавить тему вопросов по мере необходимости.

    test_number = models.IntegerField('Номер теста', unique=True)

    class Meta:
        verbose_name= 'Тест'
        verbose_name_plural = 'Тесты'
    
    def __str__(self):
        return f'Тест №{self.test_number}'


class User(models.Model):
    # Посредственная заглушка авторизации, лучше использовать полноценную, 
    #чтобы пользователи могли вернуться и посмотреть свои старые резульаты

    username = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return self.username


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    toughest_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    succes_rate = models.PositiveSmallIntegerField(default=0)
    pass_number = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Результаты теста'

    def __str__(self):
        return f'{self.username.username}  {self.test.test_number}'
    
    