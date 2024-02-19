% if business_type and business_type.name != 'default':
    <span class="icon tag neutral"><svg><use href="${request.static_url('endi:static/icons/endi.svg')}#tag"></use></svg> ${business_type.label}</span>
% endif
