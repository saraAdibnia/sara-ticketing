# reports_view
## ListOfBadOperators

_ListOfBadOperators/_

It reports list of operators who their ticket's status which they are the operator of them are 3(is_suspended)

# views
## AllTickets
_all_ticket/

To show all tickets , and for user with role = 1 ( کاربر سازمانی )  , show tickets that is for their department or they are the user or created_by of the tickets , for user with role = 2 (کاربر تحصیل دار ) and user with role 0 (کاربر عادی ) , just shows the tickets that they are the user of them  .
## List of tickets
_list_ticket/_

There is an api for getting all tickets and if request for file can retrieve them with files also able to filter tickets by : is_answered , user_id ,created_dated__date__range , title__icontains,text__icontains , department_id , ticket_id , tag_id.

## Create tickets
_create_ticket/_

if a user wants to create a ticket in this web service there are some mandatory fields **(title, text, user, sub_category, category, kind ,tags)** and many optionals(department ,operator, created_by,is_answered,  status, priority).
## Delete tickets
_delete_ticket/_

Tickets can not be deleted they can just be suspended by their id.
## List of answers
_all_answer/_

In order to get a list of answers user needs to be authenticated.If user is just a normal user they can only see answers which have been sent directly to the user.But Corporate users can see all answers for a ticket.

## CreateGeneralAnswers
_create_general_answers/

For first time to assign a ticket to an operator and answer it , this api will be called and the field operator will be filled. 
## Create answers
_create_answer/_

if a user wants to answer a ticket in this web service there are some mandatory fields **(ticket, text, sender, reciever)** and one optional(to_department).
## Delete answer
_delete_answer/_

answers can not be deleted they can just be suspended by their id.

## ListFiles
by getting answer_id or ticket_id will show the files of the ticket or answer
## CreateFiles
Can create files by getting their id for ticket(or answer if the file will be attached to answer) and the file and name of file or if the user wants , getting the url instead of file , also getting the file format. 
## PaginatedElasticSearch
an elastic search to serach in title of tickets.
## TagNormalSerach
to search in tags easily , by field search in query params.
## TicketNormalSearch
to search in tickets easily , by field search in query params.
## ReviewsListAPI
to show list of reviews by getting id of ticket in query params , or if the user wants all of the reviews ca let the params empty.
## ReviewsCreateAPI
to create a review and if an operator make a review , rated_operator will be True and if a user review rated_user will be True .
## ReactionListApi
List of reactions , by getting the id of answers , and if the id have'nt been given , all the reactions will be shown.
## ReactionCreateAPI
for creating reaction sender of answer and user must be the same .or bad request happens.
## ReactionDeleteAPI
for deleting the reaction , it gets the id of answer and it empty it (equals it to None) .
## List of Categories
_categories/_

And there is another api that can show sub of the specefic category (refrenced by id in params) or the category of  a specefic sub (refrenced by id in params).
## Create Categories
_create_category/_

To create category there is just on requierd field **(name)** but to create sub category there are two required fields **(name ,parent)**.
## Update Categories
_update_category/_

In ordere to update a category first in query params the id of category is needed and then the name of the category or the parent of the category can be updated.
## Delete categories
_delete_category/_

categories can not be deleted they can just be suspended by their id.
## List of Tags
_all_tag/_

There is an api to show all tags.
## Create Tags
_create_tag/_

if a user wants to create a tag in this web service there are two mandatory fields **(e_name, f_name)** and no optional.
## Update Tags
_update_tag/_

In ordere to update a tag first the id of the tag in query params is needed and then the e_name or the f_name of the tag can be updated.
## Delete tags
_delete_tag/_

tags can not be deleted they can just be suspended by their id.
## List of Files
_all_file/_

There is an api to show all files.
## Create Files
_create_file/_

if a user wants to upload a file in this web service there are some requierd fields **(file_field, ticket, answer)** and one optional(name).(otherwise validation error will be raised)
## Elastic search
_search/_

search a ticket by title.