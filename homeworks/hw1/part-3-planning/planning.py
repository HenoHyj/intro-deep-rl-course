# %% [markdown]
# # Planning and PDDL
# 
# This notebook examines the use of *planning* in artifical intelligence.  We will look at a classical planning algorithm called STRIPS (Standford Research Institute Problem Solver), which uses a language for defining plans called PDDL (Planning Domain Definition Language).  STRIPS, PDDL and classic planning are all defined in the Russell and Norvig textbook AI A Modern Approach, in chapter 11.  I also recommend this tutorial by Kory Becker: [Artificial Intelligence Planning with STRIPS, A Gentle Introduction](http://www.primaryobjects.com/2015/11/06/artificial-intelligence-planning-with-strips-a-gentle-introduction/).  She has an [online demo](https://stripsfiddle.herokuapp.com) that lets you upload your own PDDL-specified problems, and find solutions to them.  
# 
# 
# We will use this Python library:
# * [PDDL Parser](https://github.com/pucrs-automated-planning/pddl-parser)
# 
# In PDDL, we can define **action schema** to represent actions.  Here is an example of an action schema for flying a plane from one location to another:
# ```
# (:action fly
#      :parameters (?p - plane ?from - airport ?to - airport)
#      :precondition (and (plane ?p) (airport ?from) (airport ?to) (at ?p ?from))
#      :effect (and (at ?p ?to)) (not (at ?p ?from)))
# )
# ```
# 
# This defines an action called **fly**, which takes 3 arguments: a plane **p**, a starting airport **from** and a destination airport **to**.  In order for this action to be applied, several *preonditions* must be satisified:
# 1. **p** must be a plane
# 1. **from** must be be an airport
# 1. **to** must be be an airport
# 1. **p** must initially be located at **from**.
# 
# 
# 
# Once the action is applied, then it has the *effect* of changing several states in the world.
# 1. **p** is no longer located at **from**
# 1. **p** is now located at **to**
# 
# In general, a schema consists of:
# * an action name
# * a list of all the variables use in the schema
# * a precondition - a conjunction of literals (positive or negated atomic logical sentences)
# * an effect - a conjunction of literals
# 
# _Note: The enforcement of argument types like `(plane ?p)` can be left out of the action schema if we specify types in the domain PDDL file._
# 

# %% [markdown]
# 
# ## What to do
# 
# In this exercise, you'll be writing PDDL for action castles, and then using the PDDL Parser and its planner to come up with solutions to different challenges in the game.
# 
# To do this, you'll create pairs of files.  One file will represent the __domain__ and the other file will represent the __problem__.
# 
# The domain file will specify the __types__ of things in your game, and a set of possible __actions__.
# 
# The problem file will specify an instance of the game by giving its starting state.  For example, it will contain the list of how locations are connected, and where all of the objects are located at the start of the game.
# 

# %%
import os

def write_to_file(string, path, filename):
  """This is a helper function to create a file from a string."""
  if not os.path.exists(path) and path != "":
    os.makedirs(path)
  with open(os.path.join(path, filename), "w") as f:
      f.write(string)

# %% [markdown]
# ## Example Domain
# Here's a starting example of a PDDL for the Action Castle domain.  
# 
# ```
# (define (domain action-castle)
#    (:requirements :strips :typing)
#    (:types player location direction monster item)
# 
#    (:action go
#       :parameters (?dir - direction ?p - player ?l1 - location ?l2 - location)
#       :precondition (and (at ?p ?l1) (connected ?l1 ?dir ?l2) (not (blocked ?l1 ?dir ?l2)))
#       :effect (and (at ?p ?l2) (not (at ?p ?l1)))
#    )
# )
# ```
# This specifies 5 types of things that are in the game:
# * the player
# * locations
# * directions
# * monsters (like the troll, the guard and the ghost)
# * items
# 
# We also define one action to get you started.  The action is `go`.  It takes in 4 arguments:
# * the direction to travel in
# * the player to move
# * the starting location
# * the destination location
# 
# `Precondition` specifies what must be true in order to apply the `go` action, and `effect` specifies how the state of the world will change as a result of applying it.
# 

# %%
import os
path = os.getcwd()

# %%
domain_1 = """
(define (domain action-castle)
   (:requirements :strips :typing)
   (:types player location direction monster item)

   (:action go
      :parameters (?dir - direction ?p - player ?l1 - location ?l2 - location)
      :precondition (and (at ?p ?l1) (connected ?l1 ?dir ?l2) (not (blocked ?l1 ?dir ?l2)))
      :effect (and (at ?p ?l2) (not (at ?p ?l1)))
   )
)
"""

# Write the domain to a PDDL file
domain_filename = "domain.pddl"
write_to_file(domain_1, path, domain_filename)

# %%
!ls '{path}'

# %% [markdown]
# ## Example Problem
# 
# Here's an example of how to specify a problem called `navigate-to-location` in the `action-castle` domain.  We'll specify thee objects, which are instances of the types.  (We'll call our player the `npc` which stands for "non-playable character", to indicate that the AI is controling it, rather than us).  We'll also list out all of the locations and directions in the game.
# 
# We can introduce predicates like
# ```
# (connected cottage out gardenpath)
# ```
# or
# ```
# (at npc cottage)
# ```
# that specify the starting conditions of the game.  These can be "fluent" meaning that they can change over the course of the game by application of the actions.

# %%
problem_1 = """
(define (problem navigate-to-location)
   (:domain action-castle)

   (:objects
      npc - player
      cottage gardenpath fishingpond gardenpath windingpath talltree drawbridge courtyard towerstairs tower dungeonstairs dungeon greatfeastinghall throneroom - location
      in out north south east west up down - direction
   )

   (:init
      (connected cottage out gardenpath)
      (connected gardenpath in cottage)
      (connected gardenpath south fishingpond)
      (connected fishingpond north gardenpath)
      (connected gardenpath north windingpath)
      (connected windingpath south gardenpath)
      (connected windingpath up talltree)
      (connected talltree down windingpath)
      (connected windingpath east drawbridge)
      (connected drawbridge west windingpath)
      (connected drawbridge east courtyard)
      (connected courtyard west drawbridge)
      (connected courtyard up towerstairs)
      (connected towerstairs down courtyard)
      (connected towerstairs up tower)
      (connected tower down towerstairs)
      (connected courtyard down dungeonstairs)
      (connected dungeonstairs up courtyard)
      (connected dungeonstairs down dungeon)
      (connected dungeon up dungeonstairs)
      (connected courtyard east greatfeastinghall)
      (connected greatfeastinghall west courtyard)
      (connected greatfeastinghall east throneroom)
      (connected throneroom west greatfeastinghall)
      (at npc cottage)
   )

   (:goal (and (at npc throneroom)))
)
"""

# Write the problem to a PDDL file
problem_filename = "problem.pddl"
write_to_file(problem_1, path, problem_filename)

# %% [markdown]
# ## Check that your files are correctly formatted
# 
# You can check that your PDDL files are correctly formatted by running this command.  It will print out all of the parts of your PDDL files if they are correctly formatted, or it will thrown an Exception if you have a formatting error.
# 
# _Note: The PDDL notation goes back to the LISP programming language, which was a popular language in the early days of AI, when STRIPS was being developed.  It takes some getting used to, but hopefully it won't be too difficult for you to understand the format._

# %%
!python -B PDDL.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# ## Compute a plan
# 
# You can use the planner in the PDDL Parser package to create a plan. The plan is a sequence of actions that will take you from the start state (specified in your problem.pddl file) to the goal (specified in the same file).

# %%
!python -B planner.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# # TODO: Move Objects to Desired Location
# 
# __Domain__:
# Add two new actions to our action-castle domain PDDL:
# * `get`
# * `drop`
# 
# __Problem__:
# Create several items like the fishing pole, the rose, the crown, and put them in their starting locaiton in your problem PDDL.  Set the goal to be `(:goal (and (at crown throneroom)))`.
# 
# Check to see if the NPC can move the crown to the throne room.
# 
# 

# %%
domain_2 = """
(define (domain action-castle)
   (:requirements :strips :typing)
   (:types player location direction monster item)
   (:predicates 
        (at ?obj - object ?loc - location) ; Can apply to player or item
        (connected ?l1 - location ?dir - direction ?l2 - location)
        (blocked ?l1 - location ?dir - direction ?l2 - location)
        (inventory ?p - player ?i - item) ; Player has item
        (gettable ?i - item) ; Item can be picked up
   )

   (:action go
      :parameters (?p - player ?dir - direction ?l1 - location ?l2 - location)
      :precondition (and (at ?p ?l1) (connected ?l1 ?dir ?l2) (not (blocked ?l1 ?dir ?l2)))
      :effect (and (at ?p ?l2) (not (at ?p ?l1)))
   )

   ; TODO: implement get action
   (:action get
      :parameters (?p - player ?i - item ?l - location)
      :precondition (and (at ?p ?l) (at ?i ?l) (gettable ?i))
      :effect (and (inventory ?p ?i) (not (at ?i ?l)))
   )

   ; TODO: implement drop action
   (:action drop
      :parameters (?p - player ?i - item ?l - location)
      :precondition (and (at ?p ?l) (inventory ?p ?i))
      :effect (and (not (inventory ?p ?i)) (at ?i ?l))
   )
)
"""

# Write the domain to a PDDL file
domain_filename = "domain-2-move-objects.pddl"
write_to_file(domain_2, path, domain_filename)

# %%
problem_2 = """
(define (problem move-item-to-location)
   (:domain action-castle)

   (:objects
      npc - player
      cottage gardenpath fishingpond windingpath talltree drawbridge courtyard towerstairs tower dungeonstairs dungeon greatfeastinghall throneroom - location
      in out north south east west up down - direction
      ; TODO - add the item names here
      pole - item
      rose - item
      crown - item 
      # Need fish and branch for dependencies if we model the full path
      fish - item
      branch - item
      key - item 
      # Non-gettable items for context
      rosebush - item
      troll - monster # Use monster type
      guard - monster
      unconsciousguard - item # Represent as item state
      lockeddoor - item 
      unlockeddoor - item # Represent as item state
   )

   (:init
      (connected cottage out gardenpath)
      (connected gardenpath in cottage)
      (connected gardenpath south fishingpond)
      (connected fishingpond north gardenpath)
      (connected gardenpath north windingpath)
      (connected windingpath south gardenpath)
      (connected windingpath up talltree)
      (connected talltree down windingpath)
      (connected windingpath east drawbridge)
      (connected drawbridge west windingpath)
      (connected drawbridge east courtyard)
      (connected courtyard west drawbridge)
      (connected courtyard up towerstairs)
      (connected towerstairs down courtyard)
      (connected towerstairs up tower)
      (connected tower down towerstairs)
      (connected courtyard down dungeonstairs)
      (connected dungeonstairs up courtyard)
      (connected dungeonstairs down dungeon)
      (connected dungeon up dungeonstairs)
      (connected courtyard east greatfeastinghall)
      (connected greatfeastinghall west courtyard)
      (connected greatfeastinghall east throneroom)
      (connected throneroom west greatfeastinghall)
      
      (at npc cottage)
      
      ; TODO - add the starting locations for items here
      ; Gettable items
      (at pole cottage) (gettable pole)
      (at branch talltree) (gettable branch)
      # (at crown dungeon) - Let's assume crown starts in dungeon after ghost is dealt with
      # The basic get/drop won't model banishing ghost, so we might need to simplify 
      # or assume crown is already available somewhere else for this simple task.
      # Let's place it in the dungeon for now, assuming we navigate there.
      (at crown dungeon) (gettable crown) 
      (gettable fish) ; Fish doesn't start anywhere, it's created
      (gettable rose) ; Rose doesn't start anywhere, it's created
      (gettable key) ; Key doesn't start anywhere, it's created
      
      ; Scenery / Characters / States
      (at rosebush gardenpath) (not (gettable rosebush))
      (at troll drawbridge) 
      (at guard courtyard)
      (at lockeddoor towerstairs) (not (gettable lockeddoor))
      (not (gettable unlockeddoor)) # unlockeddoor doesn't exist initially
      (not (gettable unconsciousguard)) # guard isn't unconscious initially
      
      ; Blocks (initial state) - requires blocked predicate
      ; (blocked drawbridge east courtyard) 
      ; (blocked courtyard east greatfeastinghall)
      ; (blocked towerstairs up tower)
   )

   ; TODO - Set the goal
   (:goal (and (at crown throneroom)))
)
"""

# Write the problem to a PDDL file
problem_filename = "problem-2-move-objects.pddl"
write_to_file(problem_2, path, problem_filename)

# %% [markdown]
# ### Check your file formats
# 
# If you run this code without updating the domain and problem PDDL files, you'll get an error that says `AttributeError: 'str' object has no attribute 'pop'`.  That indicates that your PDDL format is incorrect.  

# %%
!python -B PDDL.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# ### Compute a plan

# %%
!python -B planner.py {path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# # TODO: Go Fishing
# 
# 
# __Domain Updates__:
# Add a new action schema called `gofish` that requires the fishing pole to catch a fish at a location that has a pond.
# 
# 
# __Problem Updates__:
# Add a new predicate that indicates which locations where fishing can take place.  
# ```
# (haslake fishingpond)
# ```
# Set the goal to be `(:goal (and (inventory npc fish)))`.
# 
# 
# 
# _Hints:
#  It might be helpful to create new types in your domain and problem specification like: fishingpole, and food.  This might help avoid being able to catch a fish with a rose._

# %%
domain_3 = """
(define (domain action-castle-fishing)
    (:requirements :strips :typing)
    ; Added more specific item types and lake type
    (:types player location direction monster item fishingpole food lake)

    (:predicates 
        (at ?obj - object ?loc - location) 
        (connected ?l1 - location ?dir - direction ?l2 - location)
        (blocked ?l1 - location ?dir - direction ?l2 - location)
        (inventory ?p - player ?i - item) 
        (gettable ?i - item)
        (haslake ?loc - location) ; Predicate for fishing spots
    )

    (:action go
      :parameters (?p - player ?dir - direction ?l1 - location ?l2 - location)
      :precondition (and (at ?p ?l1) (connected ?l1 ?dir ?l2) (not (blocked ?l1 ?dir ?l2)))
      :effect (and (at ?p ?l2) (not (at ?p ?l1)))
    )

    (:action get
      :parameters (?p - player ?i - item ?l - location)
      :precondition (and (at ?p ?l) (at ?i ?l) (gettable ?i))
      :effect (and (inventory ?p ?i) (not (at ?i ?l)))
    )

    (:action drop
      :parameters (?p - player ?i - item ?l - location)
      :precondition (and (at ?p ?l) (inventory ?p ?i))
      :effect (and (not (inventory ?p ?i)) (at ?i ?l))
    )
    
    ; TODO: implement gofish action
    (:action gofish
        :parameters (?p - player ?pole - fishingpole ?fish - food ?l - location)
        :precondition (and (at ?p ?l) (inventory ?p ?pole) (haslake ?l))
        ; Effect: Player now has the fish, assumes infinite fish in lake
        :effect (and (inventory ?p ?fish))
    )
)
"""

problem_3 = """
(define (problem go-fish)
   (:domain action-castle-fishing)

   (:objects
      ; TODO Define objects
      npc - player
      cottage gardenpath fishingpond - location ; Only locations needed for this problem
      in out north south - direction
      pole - fishingpole
      fish - food
   )

   (:init
      ; TODO Define initial state
      (connected cottage out gardenpath)
      (connected gardenpath in cottage)
      (connected gardenpath south fishingpond)
      (connected fishingpond north gardenpath)
      
      (at npc cottage) ; Start player at cottage
      (at pole cottage) ; Pole starts at cottage
      (gettable pole) ; Pole is gettable
      
      (haslake fishingpond) ; Define where the lake is
   )

   (:goal (and (inventory npc fish))) ; Goal is to have the fish
)
"""

# Write the problem to a PDDL file
problem_filename = "problem-3-fishing.pddl"
write_to_file(problem_3, path, problem_filename)

# Write the domain to a PDDL file
domain_filename = "domain-3-fishing.pddl"
write_to_file(domain_3, path, domain_filename)

# %%
# Check your files are formatted correctly
!python -B PDDL.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %%
# Compute a plan
!python -B planner.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# # TODO: Feed the Troll
# 
# 
# __Domain Updates__:
# Add a new action schema called `feed` that feeds food to a monster, and results in the monster no longer being hungry, and the food being gone.
# 
# 
# __Problem Updates__:
# Add a new predicate to the start state.
# ```
# (hungry troll)
# ```
# And a new goal:
# ```
#  (:goal (and (not (hungry troll))))
# ```
# 
# 
# 

# %%
domain_4 = """
(define (domain action-castle-feeding)
    (:requirements :strips :typing)
    ; Reuse types from fishing domain, add monster
    (:types player location direction monster item fishingpole food lake)

    (:predicates 
        (at ?obj - object ?loc - location) 
        (connected ?l1 - location ?dir - direction ?l2 - location)
        (blocked ?l1 - location ?dir - direction ?l2 - location)
        (inventory ?p - player ?i - item) 
        (gettable ?i - item)
        (haslake ?loc - location)
        (hungry ?m - monster) ; Predicate for hungry monsters
        (is_food ?i - item) ; Predicate to identify food items
    )

    ; Reuse go, get, drop, gofish from previous domains
    (:action go
      :parameters (?p - player ?dir - direction ?l1 - location ?l2 - location)
      :precondition (and (at ?p ?l1) (connected ?l1 ?dir ?l2) (not (blocked ?l1 ?dir ?l2)))
      :effect (and (at ?p ?l2) (not (at ?p ?l1)))
    )
    (:action get
      :parameters (?p - player ?i - item ?l - location)
      :precondition (and (at ?p ?l) (at ?i ?l) (gettable ?i))
      :effect (and (inventory ?p ?i) (not (at ?i ?l)))
    )
    (:action drop
      :parameters (?p - player ?i - item ?l - location)
      :precondition (and (at ?p ?l) (inventory ?p ?i))
      :effect (and (not (inventory ?p ?i)) (at ?i ?l))
    )
    (:action gofish
        :parameters (?p - player ?pole - fishingpole ?fish - food ?l - location)
        :precondition (and (at ?p ?l) (inventory ?p ?pole) (haslake ?l))
        :effect (and (inventory ?p ?fish))
    )
    
    ; TODO: implement feed action
    (:action feed
        :parameters (?p - player ?food - item ?m - monster ?l - location)
        :precondition (and (at ?p ?l) (at ?m ?l) (inventory ?p ?food) (hungry ?m) (is_food ?food))
        ; Effect: Monster is not hungry, food is consumed
        :effect (and (not (hungry ?m)) (not (inventory ?p ?food)))
    )
)
"""

problem_4 = """
(define (problem feed-troll)
    (:domain action-castle-feeding)
    ; TODO Define objects, initial state, and goal
    (:objects
        npc - player
        cottage gardenpath fishingpond windingpath drawbridge - location ; Relevant locations
        in out north south east west - direction
        pole - fishingpole
        fish - food
        troll - monster
    )
    
    (:init
        (connected cottage out gardenpath)
        (connected gardenpath in cottage)
        (connected gardenpath south fishingpond)
        (connected fishingpond north gardenpath)
        (connected gardenpath north windingpath)
        (connected windingpath south gardenpath)
        (connected windingpath east drawbridge)
        (connected drawbridge west windingpath)
        
        (at npc cottage) ; Player starts at cottage
        (at pole cottage) ; Pole starts at cottage
        (gettable pole)
        
        (haslake fishingpond) ; Need the lake to get fish
        (is_food fish)      ; Define fish as food
        
        (at troll drawbridge) ; Troll starts at drawbridge
        (hungry troll)       ; Troll starts hungry
    )

   (:goal (and (not (hungry troll)))) ; Goal is for troll not to be hungry
)
"""

# Write the problem to a PDDL file
problem_filename = "problem-4-feed-the-troll.pddl"
write_to_file(problem_4, path, problem_filename)

# Write the domain to a PDDL file
domain_filename = "domain-4-feed-the-troll.pddl"
write_to_file(domain_4, path, domain_filename)

# %%
# Check your files are formatted correctly
!python -B PDDL.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %%
# Compute a plan
!python -B planner.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# # Optional: Unblock Troll
# 
# Our PDDL naviation example left out blocked locations, which are an important part of the puzzle solving of text adventure games.
# 
# You can you implement a block for the troll, which is resolved after the troll is fed?
# 
# ```
# (blocked drawbridge east courtyard)
# (:goal (and (at npc tower)))
# ```
# 

# %%
domain_5 = """
TODO
"""

problem_5 = """
(define (problem unblock-troll)

TODO
(blocked drawbridge east courtyard)

   (:goal (and (at npc tower)))
"""

# Write the problem to a PDDL file
problem_filename = "problem-5-unblock-troll.pddl"
write_to_file(problem_5, path, problem_filename)

# Write the domain to a PDDL file
domain_filename = "domain-5-unblock-troll.pddl"
write_to_file(domain_5, path, domain_filename)

# %%
# Check your files are formatted correctly
!python -B PDDL.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %%
# Compute a plan
!python -B planner.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# # Optional: Unblock Guard
# 
# You can you implement a block for the guard, which is resolved after the you hit the guard with the branch?
# 
# ```
#       (at branch talltree)
#       (weapon branch)
#       (at guard courtyard)
#       (blocked courtyard east greatfeastinghall)
# 
# ```
# 

# %%
domain_6 = """
TODO
"""

problem_6 = """
(define (problem unblock-guard)

TODO

   (:goal (and (at npc tower)))
"""

# Write the problem to a PDDL file
problem_filename = "problem-6-unblock-guard.pddl"
write_to_file(problem_6, path, problem_filename)

# Write the domain to a PDDL file
domain_filename = "domain-6-unblock-guard.pddl"
write_to_file(domain_6, path, domain_filename)

# %%
# Check your files are formatted correctly
!python -B PDDL.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %%
# Compute a plan
!python -B planner.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %% [markdown]
# # Optional: Give the Rose to the Princess
# 
# The princess is locked in the tower.  Can you find the key and then bring her the rose?
# 
# 
# ```
#       (at rose gardenpath)
#       (blocked towerstairs up tower)
#       (locked tower)
#       (at princess tower)
# 
#    (:goal (and (inventory princess rose) (at npc tower)))
# ```

# %%
domain_7 = """
TODO
"""

problem_7 = """
(define (problem give-rose-to-princess)

TODO

   (:goal (and (inventory princess rose) (at npc tower)))
"""

# Write the problem to a PDDL file
problem_filename = "problem-7-give-rose-to-princess.pddl"
write_to_file(problem_7, path, problem_filename)

# Write the domain to a PDDL file
domain_filename = "domain-7-give-rose-to-princess.pddl"
write_to_file(domain_7, path, domain_filename)

# %%
# Check your files are formatted correctly
!python -B PDDL.py '{path}/{domain_filename}' '{path}/{problem_filename}'

# %%
# Compute a plan
!python -B planner.py '{path}/{domain_filename}' '{path}/{problem_filename}'


