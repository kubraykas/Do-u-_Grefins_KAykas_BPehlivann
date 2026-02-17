import streamlit as st
import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'cbam_form_config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_app():
    config = load_config()
    app_cfg = config.get('app_config', {})
    
    st.set_page_config(
        page_title=app_cfg.get('title', 'GreFins CBAM'),
        page_icon="🌱",
        layout="wide"
    )

    st.title(app_cfg.get('title'))
    st.caption(f"Versiyon: {app_cfg.get('version')} | Para Birimi: {app_cfg.get('currency')}")

    # 1. Sektör Seçimi
    sectors = config.get('sectors', {})
    sector_labels = {k: v['label'] for k, v in sectors.items()}
    
    selected_sector_key = st.selectbox(
        "Sektör Seçiniz",
        options=list(sector_labels.keys()),
        format_func=lambda x: sector_labels[x]
    )
    
    sector_data = sectors[selected_sector_key]
    
    # 2. Rota Seçimi
    routes = sector_data.get('routes', {})
    route_keys = list(routes.keys())
    route_labels = {k: v['label'] for k, v in routes.items()}
    
    st.subheader("Üretim Rotası")
    selected_route_key = st.radio(
        "Tesisinizin üretim metodunu seçiniz:",
        options=route_keys,
        format_func=lambda x: route_labels[x],
        horizontal=True
    )
    
    st.info(f"**Açıklama:** {routes[selected_route_key].get('description', 'Seçilen rota için analiz hazırlanıyor.')}")

    user_data = {
        "sector": selected_sector_key,
        "route": selected_route_key,
        "inputs": {}
    }

    # 3. Dinamik Inputlar
    st.divider()
    inputs_config = sector_data.get('inputs', {})
    
    # Grupları Expander içinde göster
    for group_key, fields in inputs_config.items():
        group_label = group_key.replace('_', ' ').title()
        with st.expander(f"📊 {group_label}", expanded=True):
            for field in fields:
                # 4. Koşullu Gösterim (show_if_route)
                if 'show_if_route' in field:
                    if selected_route_key not in field['show_if_route']:
                        continue
                
                # Widget oluşturma
                field_id = field['id']
                label = f"{field['label']} ({field.get('unit', '')})" if field.get('unit') else field['label']
                help_text = field.get('help', '')
                
                val = None
                if field['type'] == 'number_input':
                    val = st.number_input(
                        label,
                        min_value=float(field.get('min', 0.0)),
                        max_value=float(field.get('max', 1000000000.0)) if 'max' in field else None,
                        value=float(field.get('default', 0.0)),
                        help=help_text,
                        disabled=field.get('disabled', False),
                        key=f"{selected_sector_key}_{field_id}"
                    )
                elif field['type'] == 'slider':
                    val = st.slider(
                        label,
                        min_value=int(field.get('min', 0)),
                        max_value=int(field.get('max', 100)),
                        value=int(field.get('default', 50)),
                        help=help_text,
                        key=f"{selected_sector_key}_{field_id}"
                    )
                elif field['type'] == 'selectbox':
                    options = field.get('options', [])
                    option_labels = [opt['label'] for opt in options]
                    option_values = [opt['value'] for opt in options]
                    
                    selected_label = st.selectbox(
                        label,
                        options=option_labels,
                        help=help_text,
                        key=f"{selected_sector_key}_{field_id}"
                    )
                    # Değeri value olarak ata
                    val = option_values[option_labels.index(selected_label)]
                
                user_data["inputs"][field_id] = val

    # Financials
    financials = config.get('financials', {})
    with st.expander(f"💰 {financials.get('label', 'Finansal Veriler')}", expanded=False):
        for field in financials.get('inputs', []):
            field_id = field['id']
            label = f"{field['label']} ({field.get('unit', '')})" if field.get('unit') else field['label']
            
            if field['type'] == 'slider':
                val = st.slider(label, min_value=0, max_value=100, value=field.get('default', 0), key=f"fin_{field_id}")
            elif field['type'] == 'number_input':
                val = st.number_input(label, value=float(field.get('default', 0.0)), key=f"fin_{field_id}")
            
            user_data["inputs"][field_id] = val

    st.divider()
    if st.button("HESAPLA VE ANALİZ ET", type="primary", use_container_width=True):
        st.success("Veriler başarıyla toplandı. Analiz modülüne gönderiliyor...")
        st.json(user_data)
        # Burada analiz fonksiyonu çağrılabilir:
        # result = analyze_cbam(user_data)
        # st.write(result)

if __name__ == "__main__":
    run_app()
