import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About Us")

st.markdown (
    """
    &nbsp; U-Connect is a data-driven, student-centric networking platform that 
    empowers students by providing direct access to peer-generated insights 
    and experiences. Through detailed profiles showcasing academic courses, 
    co-op placements, and study-abroad opportunities, students can easily connect 
    with others who have faced similar academic and professional challenges. 
    This platform collects and analyzes real student data, helping users make 
    informed decisions about courses, co-ops, and career paths.
    
    """
        )
