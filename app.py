import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta

# Sample data generation with more detailed information
def generate_sample_data():
    devices = [
        {
            "device_id": "P001", 
            "tipo": "Impresora", 
            "model": "HP LaserJet", 
            "total_copies": 15000, 
            "costo_mantenimiento": 500, 
            "ingreso_arrendamiento": 2000,
            "inicio_arrendamiento": datetime(2024, 1, 1),
            "final_arrendamiento": datetime(2024, 12, 31),
            "status": "Activo",
            "cliente": "Compañía A"
        },
        {
            "device_id": "P002", 
            "tipo": "Impresora", 
            "model": "Canon ImageRUNNER", 
            "total_copies": 22000, 
            "costo_mantenimiento": 750, 
            "ingreso_arrendamiento": 2500,
            "inicio_arrendamiento": datetime(2024, 2, 15),
            "final_arrendamiento": datetime(2024, 11, 15),
            "status": "Activo",
            "cliente": "Compañía B"
        },
        {
            "device_id": "C001", 
            "tipo": "Computadora", 
            "model": "Dell Latitude", 
            "total_copies": 0, 
            "costo_mantenimiento": 300, 
            "ingreso_arrendamiento": 1500,
            "inicio_arrendamiento": datetime(2024, 3, 1),
            "final_arrendamiento": datetime(2024, 12, 31),
            "status": "Activo",
            "cliente": "Compañía C"
        },
        {
            "device_id": "C002", 
            "tipo": "Computadora", 
            "model": "MacBook Pro", 
            "total_copies": 0, 
            "costo_mantenimiento": 450, 
            "ingreso_arrendamiento": 1800,
            "inicio_arrendamiento": datetime(2024, 1, 15),
            "final_arrendamiento": datetime(2024, 10, 15),
            "status": "Mantenimiento",
            "cliente": "Compañía D"
        }
    ]
    return pd.DataFrame(devices)

# Calculate ROI for each device
def calculate_roi(df):
    df['roi'] = (df['ingreso_arrendamiento'] - df['costo_mantenimiento']) / df['costo_mantenimiento'] * 100
    return df

# Streamlit Dashboard
def main():
    st.set_page_config(page_title="Device Rental Monitoring Dashboard", layout="wide")
    
    # Title and Overview
    st.title("Sistema de monitoreo de alquiler de dispositivos")
    
    # Generate and process sample data
    df = generate_sample_data()
    df = calculate_roi(df)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Resumen del Tablero", 
        "Análisis de ROI y Finanzas", 
        "Gestión de Dispositivos", 
        "Seguimiento de Alquileres"
    ])
    
    # Dashboard Overview Tab
    with tab1:
        st.header("Descripción general del sistema")
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de dispositivos", len(df))
        with col2:
            st.metric("Ingreso mensual total", f"${df['ingreso_arrendamiento'].sum():,.2f}")
        with col3:
            st.metric("Costo de mantenimiento total", f"${df['costo_mantenimiento'].sum():,.2f}")
        with col4:
            st.metric("Dispositivos activos", len(df[df['status'] == 'Active']))
        
        # Device Status Pie Chart
        st.subheader("Distribución del estado del dispositivo")
        status_counts = df['status'].value_counts()
        fig_status = px.pie(
            names=status_counts.index, 
            values=status_counts.values,
            title='Descripción general del estado del dispositivo',
            hole=0.3
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    # ROI & Financial Analysis Tab
    with tab2:
        st.header("Análisis de ROI y Finanzas")
        
        # ROI Bar Chart
        st.subheader("ROI por dispositivo")
        fig_roi = px.bar(
            df, 
            x='device_id', 
            y='roi', 
            color='tipo',
            title='Retorno de la inversión (ROI)',
            labels={'roi': 'ROI (%)', 'device_id': 'id de dispositivo'},
            color_discrete_map={'Impresora': 'blue', 'Computadora': 'green'}
        )
        st.plotly_chart(fig_roi, use_container_width=True)
        
        # Operating Cost Pie Chart
        st.subheader("Distribución de costos de mantenimiento")
        fig_cost = px.pie(
            df, 
            values='costo_mantenimiento', 
            names='device_id',
            title='Costos de mantenimiento por dispositivo',
            hole=0.3
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    
    # Device Management Tab
    with tab3:
        st.header("Gestión de inventario de dispositivos")
        
        # Device Filter
        device_tipo_filter = st.multiselect(
            "Filtrar por tipo de dispositivo", 
            options=df['tipo'].unique(),
            default=df['tipo'].unique()
        )
        
        # Filtered DataFrame
        filtered_df = df[df['tipo'].isin(device_tipo_filter)]
        
        # Detailed Device Table
        st.dataframe(filtered_df[['device_id', 'tipo', 'model', 'status', 'cliente', 'ingreso_arrendamiento', 'costo_mantenimiento']])
        
        # Quick Device Status Update
        st.subheader("Actualizar el estado del dispositivo")
        device_select = st.selectbox("Seleccionar dispositivo", df['device_id'].tolist())
        new_status = st.selectbox("Nuevo Estado", ["Activo", "Mantenimiento", "Inactivo"])
        if st.button("Estado de actualización"):
            st.success(f"Estado de {device_select} actualizado a {new_status}")
    
    # Lease Tracking Tab
    with tab4:
        st.header("Gestión de arrendamientos")
        
        # Lease Expiration Warning
        st.subheader("Próximos vencimientos de arrendamiento")
        current_date = datetime.now()
        df['dias_para_vencimiento'] = (df['final_arrendamiento'] - current_date).dt.days
        
        expiring_soon = df[df['dias_para_vencimiento'] <= 60]
        if not expiring_soon.empty:
            st.warning("Dispositivos con contratos de arrendamiento que vencen en los próximos 60 días:")
            st.dataframe(expiring_soon[['device_id', 'tipo', 'cliente', 'inicio_arrendamiento', 'final_arrendamiento', 'dias_para_vencimiento']])
        else:
            st.info("No leases expiring in the next 60 days.")
        
        # Lease Summary
        st.subheader("Resumen del contrato de arrendamiento")
        lease_summary = df.groupby('tipo').agg({
            'device_id': 'count',
            'ingreso_arrendamiento': 'sum',
            'inicio_arrendamiento': 'min',
            'final_arrendamiento': 'max'
        }).reset_index()
        st.dataframe(lease_summary)

if __name__ == "__main__":
    main()