create view dof.vw_horizontal_acc
as
  select case tolerance
           when -1 then 'unknown'
           else tolerance
                || ' '
                || uom
         end as accuracy,
         code
  from   dof.horizontal_acc ha
         join dof.tolerance_uom tu
           on ha.tolerance_uom_id = tu.id;

create view dof.vw_lighting
as
  select description,
         code
  from   dof.lighting;

create view dof.vw_marking
as
  select description,
         code
  from   dof.marking;

 create view dof.vw_obstacle_type
as
  select type,
         id
  from   dof.obstacle_type;

create view dof.vw_states_countries
as
  select code,
         name,
         'country' as type
  from   dof.oas o
         join dof.country c
           on c.oas_code = o.code
  union
  select code,
         name,
         'us_state' as type
  from   dof.oas o
         join dof.us_state us
           on us.oas_code = o.code
  order  by type desc,
            name asc;

create view dof.vw_verif_status
as
  select description,
         code
  from   dof.verif_status;

create view dof.vw_vertical_acc
as
  select case tolerance
           when -1 then 'unknown'
           else tolerance
                || ' '
                || uom
         end as accuracy,
         code
  from   dof.vertical_acc va
         join dof.tolerance_uom tu
           on va.tolerance_uom_id = tu.id;
