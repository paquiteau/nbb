===============
Next Bus Bot
===============

A bot/ cli tool that simply gives you the waiting times for next buses at your favorite bus stop.

It works only for the IDFM/RATP Network, relying on the api ``lines/v4``. For now only a handfull of bus stops on the Plateau de Saclay are registered, but you can add your own


.. warning::

   This is a personal toy project for learning new stuff in python (Python packaging, TDD, CLI tools, etc ...).
   It *might* feel overengineered, if so, it's on purpose.

   I am not responsible if you arrive late at your work.
   For serious travel planning, use your favorite app.

Example
-------
::

   $ nbb mdv
   Next buses at Mare du Vivier:
   - ⏰  6 min. (12:29)  9️⃣ 🚍 ▶ Centre Commercial Ulis 2
   - ⏰ 27 min. (12:50)  9️⃣ 🚍 ▶ Gare de Jouy en Josas
   - ⏰ 35 min. (12:58)  9️⃣ 🚍 ▶ Centre Commercial Ulis 2
   - ⏰ 53 min. (13:16)  9️⃣ 🚍 ▶ Christ de Saclay


Installation
============

Pip Installation
----------------

::

   $ pip install next-bus-bot


Developer Installation
----------------------

1. clone the repo ::

   $ git clone git@github.com:paquiteau/nbb/

2. create your venv with your favorite tool
3. Install locally the package with bells and whistles ::

   $ (venv) pip install -e .[dev,test]

4. Run tests ::

   $ pytest



TODO
----
 - automatic aliasing of stops (based on initials )
 - support for direction filtering
 - publish on PyPi
 - Add support for a bot front-end (slack, discord, IRC, etc).
 - Extend the useful bus stops.

Configuration
=============

nbb can be configured via its command line argument, or via a config file `nbb_conf.toml`, it uses `TOML https://toml.io/en/` syntax formatting. Suitable location for the config file are, loaded in this order:

 1. `nbb/nbb_conf.toml`
 2. `~/.config/nbb_conf.toml`
 3. `nbb_conf.toml` in current directory.
 4. `nbb --config <file>`


An example (and default) config file is available in `nbb/nbb_conf.toml`.
