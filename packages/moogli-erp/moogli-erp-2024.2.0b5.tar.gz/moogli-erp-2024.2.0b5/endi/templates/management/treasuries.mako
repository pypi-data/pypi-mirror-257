<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/searchformlayout.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="company_list_badges"/>

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

<div class='content_vertical_double_padding'>
    <h3>Trésoreries au ${api.format_date(treasuries_date)} - ${nb_results} enseignes</h3>
</div>

<div>
    <div class="table_container scroll_hor">
        <table class="hover_table">
            <thead>
                <tr>
                    <th scope="col" class="col_text min10">Enseigne</th>
                    % for header in treasury_headers:
                    <th scope="col" class="col_text" title="${header}">
                        ${header}
                    </th>
                    % endfor
                </tr>
            </thead>
            <tbody>
                % for company, treasury_values in treasury_data:
                    <tr>
                        <th scope="row" class="col_text min10">
                            <% company_url = request.route_path('/companies/{id}', id=company.id) %>
                            <a href="${company_url}">${company.full_label}</a> 
                            <small>${company_list_badges(company)}</small>
                        </th>
                        % for value in treasury_values:
                        <td class="col_number">
                            ${api.format_float(value, 2)}&nbsp;€
                        </td>
                        % endfor
                    </tr>
                % endfor
            </tbody>
        </table>
    </div>
</div>

</%block>
