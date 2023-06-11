## CRUD для сущностей

#### Позитив (общий сценарий)

1. Создать сущность
2. Посмотреть сущность
3. Отредактировать сущность
4. Посмотреть сущность
5. Удалить сущность
6. Посмотреть сущность (статус код НЕ 200)

#### Альтернатива на просмотр getItems (общий сценарий)

Предусловие: в систеие > 1-ой сущности  
ОР: отображается список из существующих сущностей

#### Проверка правил:

***Teacher and Student***

* `[neg]`на создание (create): Нельзя создать двух учителей/студентов с одинаковыми email-ми

1. Созать учителя/студента
2. Создать второго учителя/студента с таким же email  
   ОР: Статус код 400; body: {"error": "An error occurred. Please review your output and try again."}

* `[neg]`на редактирование (update): Нельзя редактировать email  
  Предусловие: в системе существует учитель/студент

1. Поменять email учителя/студента на существующий  
   ОР: Статус код 400; body: {"error": "You can't update the email address field."}

***Subject***

* `[neg]`на создание/редактирование (create/update): Учитель, назначаемый на предмет должен существовать в системе  
  `[neg]` Создание/редактирование предмета с НЕ существующим id-м учителя

#### Остальные проверки

* на создание: валидация полей (`[pos]`/`[neg]`)  
  _Teacher_
    * first_name*: str; [1; 50]
    * last_name*: str; [1; 50]
    * email_address*: EmailStr; max = 255  
      _Subject_
    * name*: str; [1; 50]
    * teacher_id*: str; [1; 50]
    * description*: str; max = 255  
      _Student_
    * first_name*: str; [1; 50]
    * last_name*: str; [1; 50]
    * email_address*: EmailStr; max = 255
    * major_id
    * minors
* на просмотр  
  Просмотр НЕ существующих сущностей (не существующий id-к)  
  ОР: статус код 404; body: {"error": "A teacher with ID TC145 does not exist."}
* на редактирование: валидация полей (`[pos]`/`[neg]`)   
  _Teacher_
    * first_name: str; [1; 50]
    * last_name: str; [1; 50]
    * email_address: EmailStr; max = 255  
      _Subject_
    * name: str; [1; 50]
    * teacher_id: id-к учителя
    * description: str; [0; 150]
      _Student_
    * first_name: str; [1; 50]
    * last_name: str; [1; 50]
    * email_address: EmailStr; max = 255
    * major_id: не более 1-го id-ка предмета
    * minors: id-ки предметов
* на удаление  
  Удаление НЕ существующих сущностей (не существующий id-к)  
  ОР: статус код 404; body: {"error": "A teacher with ID TC145 does not exist."}

