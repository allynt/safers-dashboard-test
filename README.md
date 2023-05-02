# safers-dashboard-test

- [safers-dashboard-test](#safers-dashboard-test)
  - [Components](#components)
    - [safers-db](#safers-db)
    - [safers-auth](#safers-auth)
## Components

### safers-db

**PostGIS** database for safers-dashboard-api

### safers-auth

**FusionAuth** for authentication.  This can be run locally for development (but not much else will work in safers b/c all the other components need to authenticate against tokens generated from the deployed FusionAuth instance of FusionAuth).

When run locally, the local **PostGRES** databse must also be run.

The local instance of **FusionAuth** is bootstrapped using **kickstart**.  Kickstart will only run if the default API Key is unset.  This means that even if you change the "auth/kickstart.json" file you will have to manually recreate the "safers-auth-db" instance in order to reset the database.  I run `docker container ls | grep safers-auth | awk '{print $1}' | xargs docker rm --force`.

When using the local instance of **FusionAuth**, you will need to populate "auth/.env".

If bootstrapping succeeds, you should see the following sort of output:

```
--------------------------------------------------------------------------------------
----------------------------------- Kickstarting ? -----------------------------------
--------------------------------------------------------------------------------------
io.fusionauth.api.service.system.kickstart.KickstartRunner - Summary:
- Created API key ending in [...HSnO]
- Completed [POST] request to [/api/tenant/<tenant-id>]
- Completed [POST] request to [/api/application/<applications-id>]
- Completed [POST] request to [/api/user/registration/]
```

The **FusionAuth** Admin should be available at "http://localhost:9011".  

Note that this local version of **FusionAuth** is purely for development purposes and testing authentication.  Most of the rest of **safers** will _not_ work unless you use the deployed instance of **FusaionAuth**.