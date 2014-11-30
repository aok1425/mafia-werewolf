# Mafia (or Werewolf)

This webapp facilitates player signing up and the distribution of roles. An added benefit of this webapp is that players can secretly choose the role they want.

## How to use:
With one player per device, have each player visit [mafiaalex.herokuapp.com](mafiaalex.herokuapp.com). The player inputs his or her name, then waits for everyone else to sign up. 

The narrator visits [mafiaalex.herokuapp.com/host](mafiaalex.herokuapp.com/host) and waits for all players to sign up. The narrator chooses the number of mafia, sheriffs, and angels, then presses Assign Roles.

The player presses View Role, and sees his or her identity.

## More details:

* You need to manually refresh on the host page.
* When players are choosing roles, priority is given to the person who signs up first.
* When the narrator is assigning roles, only players who have signed up in the past 5 minutes are shown.

## Next steps:
* Randomize priority when players choose preferred roles.
* When the narrator is choosing the number of mafia and other roles, set default settings for each number of players instead of the default always being the left choice.
* Make the preferred role form on the sign in page conform to Bootstrap specifications.
* Allow voting via the webapp? Have a timer on the webapp for each round?