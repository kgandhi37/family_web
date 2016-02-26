# Family Site

## Project built as a site for family events

Current features include: 
* Full user system including admin priviledges 
* Add locations for events 
* Add events 
* Add event "idols" - basically the guest of honour
* Add Testimonials for the guest of honour

Currently only admins can register users as this is a family site.

Once app is installed, to create first user and login please visit /initial on the browser. After that - login, add users, locations and create an event! 

At present idols can only be from the user list and testimonials are only allowed to be added for the most recent event.

Planned Future updates:

1. Ability to edit events.
1. Update the way password reset is handled - use a seperate table in database and set expiry timestamps
1. Seperate controllers further - for example have the locations handled in a location controller
1. Don't have is_admin in session, instead use a query to get user info. Safer this way
1. Add a message board system with the ability to start a thread and users to comment