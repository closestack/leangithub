    def _get_actions_from_matches(self,
                                  scenario_version,
                                  combined_matches,
                                  mode,
                                  action_spec):

        actions = []
        for is_switch_mode, matches in combined_matches:
            new_mode = mode
            if is_switch_mode:
                new_mode = ActionMode.UNDO \
                    if mode == ActionMode.DO else ActionMode.DO

            template_schema = \
                TemplateSchemaFactory().template_schema(scenario_version)

            for match in matches:
                match_action_spec = self._get_action_spec(action_spec, match)
                match_action_spec_transform = copy.deepcopy(match_action_spec)
                items_ids = [match_item[1].vertex_id for match_item in match.items()]
                match_hash = hash(tuple(sorted(items_ids)))
                self._evaluate_property_functions(template_schema, match,
                                                  match_action_spec_transform.properties)
                actions.append(ActionInfo(match_action_spec_transform, new_mode,
                                          match_action_spec_transform.id, match_hash))

        return actions
