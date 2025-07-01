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

create or replace view dof.vw_obstacle
as
	select o.oas_code,
		   oas.name as ctry_state_name,
		   o.obst_number,
		   o.verif_status_code,
		   vs.description as verif_status_desc,
		   o.type_id as obst_type_id,
		   ot.type as obst_type_desc,
		   o.lighting_code,
		   li.description as lighting_desc,
		   o.marking_code,
		   m.description as marking_desc,
		   o.hor_acc_code,
		   case hacc.tolerance
		   	 when -1 then 'unknown'
			 else hacc.tolerance
			      || ' '
				  || tu_hacc.uom
			 end as hor_acc,
		   case vacc.tolerance
		   	  when -1 then 'unknown'
			  else vacc.tolerance
			       || ' '
				   || tu_vacc.uom
			  end as vert_acc,
		   city,
		   quantity,
		   agl,
		   amsl,
		   faa_study_number,
		   action,
		   julian_date,
		   valid_from,
		   valid_to,
		   ST_AsLatLonText(location::geometry, 'D-M-S.SSSC') as latlon_dms
	from dof.obstacle o
		 join dof.oas on oas.code = o.oas_code
		 join dof.verif_status as vs on vs.code = o.verif_status_code
		 join dof.obstacle_type as ot on ot.id = o.type_id
		 join dof.lighting as li on li.code = o.lighting_code
		 join dof.marking as m on m.code = o.marking_code
		 join dof.horizontal_acc as hacc on hacc.code = o.hor_acc_code
		 join dof.vertical_acc as vacc on vacc.code = o.vert_acc_code
		 join dof.tolerance_uom as tu_hacc on tu_hacc.id = hacc.tolerance_uom_id
		 join dof.tolerance_uom as tu_vacc on tu_vacc.id = vacc.tolerance_uom_id
