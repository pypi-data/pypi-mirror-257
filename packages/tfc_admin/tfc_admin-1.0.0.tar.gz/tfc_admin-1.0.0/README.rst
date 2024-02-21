=============
**tfc_admin**
=============

Overview
--------

Make Terraform Cloud API calls for common platform administration tasks.

Available Functions
-------------------

- Show organization details
- List projects
- Get project ID from project name
- List workspaces in a project
- Get workspace ID from workspace name
- Move workspace into a project

Examples
--------

.. code-block:: PYTHON

   import tfc_admin

   project_workspaces = tfc_admin.get_project_ws(
      "my_tfc_token",
      "my_tfc_organization",
      tfc_admin.get_project_id(
         "my_tfc_token",
         "my_tfc_organization",
         "my_project_name"
      )
   )

   print(project_workspaces)
