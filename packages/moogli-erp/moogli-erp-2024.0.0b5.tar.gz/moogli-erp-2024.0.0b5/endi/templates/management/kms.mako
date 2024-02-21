<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/searchformlayout.mako" import="searchform"/>

<%block name='actionmenucontent'>
<div class='layout flex main_actions'>
    <div role='group'></div>
    <div role='group'>
        <a class='btn' href='${export_xls_url}' title="Export au format Excel (xls) dans une nouvelle fenêtre" aria-label="Export au format Excel (xls) dans une nouvelle fenêtre">
            ${api.icon('file-excel')} Excel
        </a>
        <a class='btn' href='${export_ods_url}' title="Export au format Open Document (ods) dans une nouvelle fenêtre" aria-label="Export au format Open Document (ods) dans une nouvelle fenêtre">
            ${api.icon('file-spreadsheet')} ODS
        </a>
    </div>
</div>
</%block>

<%block name='content'>

<div class='search_filters'>
    ${form|n}
</div>

<div>
    <div class="table_container scroll_hor">
        <table class="hover_table">
            <thead>
                <tr>
                    <th scope="col" class="col_text min10">&nbsp;</th>
                    %for year, month in months:
                        <th scope="col" class="col_number" colspan=2>
                            <center>${api.short_month_name(month)} ${str(year)[2:]}</center>
                        </th>
                    %endfor
                    <th scope="col" class="col_number" colspan=2><center>TOTAL</center></th>
                </tr>
                <tr>
                    <th scope="col" class="col_text min10">Salarié</th>
                    %for year, month in months:
                        <th scope="col" class="col_number"><small>N<span class="screen-reader-text">om</span>b<span class="screen-reader-text">re de</span>&nbsp;k<span class="screen-reader-text">ilo</span>m<span class="screen-reader-text">ètre</span>s</small></th>
                        <th scope="col" class="col_number"><small>Taux</small></th>
                    %endfor
                    <th scope="col" class="col_number" title="Total des kilomètres validés dans de MooGLi en ${year}">
                        Total&nbsp;k<span class="screen-reader-text">ilo</span>m<span class="screen-reader-text">ètre</span>s
                    </th>
                    <th scope="col" class="col_number" title="Total des kilomètres remboursés en ${year}">
                        Total remboursé
                    </th>
                </tr>
                <tr class="row_recap">
                    <th class="col_text min10">TOTAL (${users.count()} salariés)</th>
                    <% total_kms = 0 %>
                    <% total_amount = 0 %>
                    %for month_kms, month_amount in aggregate_data:
                        <th scope="col" class="col_number">
                            ${api.remove_kms_training_zeros(api.format_amount(month_kms))}
                        </th>
                        <th scope="col" class="col_number">&nbsp;</th>
                        <% total_kms += month_kms %>
                        <% total_amount += month_amount %>
                    %endfor
                    <th scope="col" class="col_number">
                        ${api.remove_kms_training_zeros(api.format_amount(total_kms))}
                    </th>
                    <th scope="col" class="col_number">
                        ${api.format_amount(total_amount, precision=2)}&nbsp;€
                    </th>
                </tr>
            </thead>
            <tbody>
                % for user in users:
                    <tr>
                        <th scope="row" class="col_text min10">
                            ${api.format_account(user)}
                        </th>
                        <% total_kms = 0 %>
                        <% total_amount = 0 %>
                        % for nb_kms, amount, rate in kms_data[user.id]:
                            <td class="col_number">${api.remove_kms_training_zeros(api.format_amount(nb_kms))}</td>
                            <td class="col_number"><small>${rate}</small></td>
                            <% total_kms += nb_kms %>
                            <% total_amount += amount %>
                        % endfor
                        <th class="col_number">
                            ${api.remove_kms_training_zeros(api.format_amount(total_kms))}
                        </th>
                        <th class="col_number">
                            ${api.format_amount(total_amount, precision=2)}&nbsp;€
                        </th>
                    </tr>
                %endfor
            </tbody>
        </table>
    </div>
</div>
</%block>
