<%! from datetime import datetime %>

${"##"} Updated: ${ln_date.strftime('%m/%d/%Y %H:%M:%S %p')}

${"##"} Info

- Last tag: ${ln_last}
- Released: ${ln_count_tags}

${"##"} Versions
% for item in ln_list_tags:
- Version: ${item.name} (${datetime.fromtimestamp(item.commit.committed_date).strftime('%d/%m/%Y')})
% endfor

% for tag in ln_group_commits:

    % if tag['commits']:
        % if tag['name'] == 'HEAD':
            ${"###"} HEAD (${ln_date.strftime('%d/%m/%Y')})
        % else:
            ${"###"} Version: ${tag['name']} (${datetime.fromtimestamp(tag['date']).strftime('%d/%m/%Y')})
        % endif
    % endif

    % for group in tag['group']:

        % if group['commits']:
            ${"####"} ${group['name']}

            % for commit in group['commits']:
                - ${commit['clean']}
            % endfor
        % endif

    % endfor
% endfor

