# List of tickets
_all_ticket/_

There is an api for getting all tickets and if request for file can retrieve them with files also able to filter tickets by : is_answered , user_id ,created_dated__date__range , title__icontains,text__icontains , department_id , ticket_id , tag_id.
# Create tickets
_create_ticket/_

if a user wants to create a ticket in this web service there are some mandatory fields **(title, text, user, sub_category, category, kind ,tags)** and many optionals(department ,operator, created_by,is_answered,  status, priority).
# Delete tickets
_delete_ticket/_

Tickets can not be deleted they can just be suspended by their id.
# List of answers
_all_answer/_

In order to get a list of answers user needs to be authenticated.If user is just a normal user they can only see answers which have been sent directly to the user.But Corporate users can see all answers for a ticket.
# Create answers
_create_answer/_

if a user wants to answer a ticket in this web service there are some mandatory fields **(ticket, text, sender, reciever)** and one optional(to_department).
# Delete answer
_delete_answer/_

answers can not be deleted they can just be suspended by their id.
# List of Categories
_categories/_

And there is another api that can show sub of the specefic category (refrenced by id in params) or the category of  a specefic sub (refrenced by id in params).
# Create Categories
_create_category/_

To create category there is just on requierd field **(name)** but to create sub category there are two required fields **(name ,parent)**.
# Update Categories
_update_category/_

In ordere to update a category first in query params the id of category is needed and then the name of the category or the parent of the category can be updated.
# Delete categories
_delete_category/_

categories can not be deleted they can just be suspended by their id.
# List of Tags
_all_tag/_

There is an api to show all tags.
# Create Tags
_create_tag/_

if a user wants to create a tag in this web service there are two mandatory fields **(e_name, f_name)** and no optional.
# Update Tags
_update_tag/_

In ordere to update a tag first the id of the tag in query params is needed and then the e_name or the f_name of the tag can be updated.
# Delete tags
_delete_tag/_

tags can not be deleted they can just be suspended by their id.
# List of Files
_all_file/_

There is an api to show all files.
# Create Files
_create_file/_

if a user wants to upload a file in this web service there are some requierd fields **(file_field, ticket, answer)** and one optional(name).(otherwise validation error will be raised)
# Elastic search
_search/_

search a ticket by title.