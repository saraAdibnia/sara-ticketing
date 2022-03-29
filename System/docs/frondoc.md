# List of tickets
There is an api for getting all tickets and there is anothere api that can filter tickets by : is_answered , user_id ,created_dated__date__range , title__icontains,text__icontains , department_id , ticket_id , tag_id.
# Create tickets
if a user wants to create a ticket in this web service there are some mandatory fields **(title, text, user, sub_category, category, kind)** and many optionals(department ,operator, created_by, tags,is_answered,  status, priority).
# Delete tickets
Tickets can not be deleted they can just be suspended by their id.
# List of answers
In order to get a list of answers user needs to be authenticated.If user is just a normal user they can only see answers which have been sent directly to the user.But coporate users can see all answers for a ticket.
# Create answers
if a user wants to answer a ticket in this web service there are some mandatory fields **(ticket, text, sender, reciever)** and one optional(to_department).
# Delete answer
answers can not be deleted they can just be suspended by their id.
# List of Categories
There is an api to show all categories. and there is another api that can show sub of the specefic category (refrenced by id in params) or the category of  a specefic sub (refrenced by id in params).
# Create Categories
To create category there is just on requierd field **(name)** but to create sub category there are two required fields **(name ,parent)**.
# Update Categories
In ordere to update a category first in query params the id of category is needed and then the name of the category or the parent of the category can be updated.
# Delete categories
categories can not be deleted they can just be suspended by their id.
# List of Tags
There is an api to show all tags.
# Create Tags
if a user wants to create a tag in this web service there are two mandatory fields **(e_name, f_name)** and no optional.
# Update Tags
In ordere to update a tag first in query params the id of tag is needed and then the e_name or the f_name of the tag can be updated.
# Delete tags
tags can not be deleted they can just be suspended by their id.
# List of Files
There is an api to show all files.
# Create Files
if a user wants to upload a file in this web service there are some requierd fields **(file_field, ticket, answer)** and one optional(name).
