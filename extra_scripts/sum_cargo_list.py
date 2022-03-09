def get_sum_of_all_cargo(wb_list):
    r = {}
    if len(wb_list) < 0:
        return r

    r['mass_weight'] = sum([w.get_weight_volume().get('completed_mass_weight', w.get_weight_volume().get('mass_weight'))
                            for w in wb_list])

    r['volume_weight'] = sum([w.get_weight_volume().get('completed_volume_weight', w.get_weight_volume().get('volume_weight'))
                              for w in wb_list])

    r['wpx_count'] = sum([w.get_weight_volume().get('completed_wpx_count', w.get_weight_volume().get('wpx_count'))
                          for w in wb_list])

    r['dox_count'] = sum([w.get_weight_volume().get('completed_dox_count', w.get_weight_volume().get('dox_count'))
                          for w in wb_list])
    return r
