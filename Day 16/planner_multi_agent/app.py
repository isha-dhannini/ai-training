import streamlit as st
from workflow import build_graph

st.set_page_config(
    page_title="Multi-Agent Planner",
    layout="wide"
)

st.title("Multi-Agent Research Assistant")

goal = st.text_area(
    "Enter your goal",
    placeholder="e.g., Deep dive analysis on the impact of quantum computing on modern RSA encryption...",
    height=120
)

if st.button("Run Workflow", type="primary"):
    if not goal.strip():
        st.warning("Please provide a valid goal statement before running.")
    else:
        # Initialize LangGraph compilation
        graph = build_graph()

        initial_state = {
            "goal": goal,
            "tasks": [],
            "results": [],
            "critique": "",
            "iterations": 0,
            "approved": False
        }

        with st.spinner("Agents are strategizing, executing, and validating your task..."):
            final_state = graph.invoke(initial_state)

        st.success("Multi-Agent Workflow Completed Successfully!")

        # Layout Columns for split display
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Final Action Plan")
            for idx, task in enumerate(final_state.get("tasks", []), start=1):
                st.markdown(f"**{idx}.** {task}")
            
            st.divider()
            
            st.subheader("Critic Assessment")
            critique = final_state.get("critique")
            if final_state.get("approved"):
                st.info(critique if critique else "The final review passed evaluation directly!")
            else:
                st.error(critique)

        with col2:
            st.subheader("Compiled Research Logs")
            tasks = final_state.get("tasks", [])
            results = final_state.get("results", [])
            
            for i, result in enumerate(results, start=1):
                task_title = tasks[i-1] if i-1 < len(tasks) else f"Task {i}"
                with st.expander(f" Task {i}: {task_title[:60]}...", expanded=(i==1)):
                    st.write(result)