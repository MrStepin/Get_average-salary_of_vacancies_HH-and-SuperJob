# Programming vacancies compare  
This script get average salary of vacancies from hh.ru and superjob.ru in Moscow   
Version: Python 3

### How to install  
Before use script create file via NotePad++ with name .env and insert to them secret key from you superjob account.   
Like this ```secret_key=v3.r.124......```  
Insert names of vacancies what you need to:  
```LIST_OF_NAMES_OF_VACANCIES = ["Программист Python", ....]```   
Then execute script via command line  

### How it works  

```C:\Users>hh_sj_v2.py"
Пожалуйста подождите, идет обработка вакансий с SuperJob.
Вакансии Python обработаны!
Вакансии C# обработаны!
Вакансии Java обработаны!
Вакансии C++ обработаны!
Вакансии JavaScript обработаны!
+SuperJob Moscow--------+---------------------+----------------------+-------------------------------+-----------------------+
| Язык программирования | Количество вакансий | Страниц с вакансиями | Выбрано вакансий для подсчёта | Средняя зарплата РУБ. |
+-----------------------+---------------------+----------------------+-------------------------------+-----------------------+
| Python                | 62                  | 4                    | 62                            | 31951                 |
| C#                    | 49                  | 3                    | 49                            | 44295                 |
| Java                  | 56                  | 3                    | 56                            | 32750                 |
| C++                   | 37                  | 2                    | 37                            | 50778                 |
| JavaScript            | 104                 | 6                    | 104                           | 42654                 |
+-----------------------+---------------------+----------------------+-------------------------------+-----------------------+```
