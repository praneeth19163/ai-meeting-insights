import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Text Analyzer", layout="wide")

st.title("📝 Text Analysis Tool")
st.markdown("Summarize long texts and extract action items & key decisions")

# API endpoint
API_URL = "http://localhost:8000"

# Text input
text_input = st.text_area(
    "Enter your long text here:",
    height=300,
    placeholder="Paste your meeting notes, article, or any long text here..."
)

# Show text stats when text is entered
if text_input.strip():
    try:
        analyze_response = requests.post(
            f"{API_URL}/analyze-text",
            json={"text": text_input}
        )
        if analyze_response.status_code == 200:
            stats = analyze_response.json()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Character Count", stats["text_length"])
            with col2:
                st.metric("Word Count", stats["word_count"])
    except:
        pass

if st.button("🚀 Analyze Text", type="primary"):
    if not text_input.strip():
        st.error("Please enter some text to analyze")
    else:
        with st.spinner("Processing..."):
            try:
                # Step 1: Generating summary and extracting items
                st.info("Step 1: Generating summary...")
                response = requests.post(
                    f"{API_URL}/analyze-combined",
                    json={"text": text_input}
                )
                response.raise_for_status()
                data = response.json()
                
                summary = data["summary"]
                extract_data = {
                    "action_items": data["action_items"],
                    "key_decisions": data["key_decisions"],
                    "input_tokens": data["extract_input_tokens"],
                    "output_tokens": data["extract_output_tokens"]
                }
                summary_data = {
                    "input_tokens": data["summary_input_tokens"],
                    "output_tokens": data["summary_output_tokens"]
                }
                
                # Display results
                st.success("✅ Analysis complete!")
                
                st.markdown("### 📊 Token Usage")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Summary Input", summary_data.get("input_tokens", 0))
                with col2:
                    st.metric("Summary Output", summary_data.get("output_tokens", 0))
                with col3:
                    st.metric("Extract Input", extract_data.get("input_tokens", 0))
                with col4:
                    st.metric("Extract Output", extract_data.get("output_tokens", 0))
                
                # col1, col2 = st.columns(2)
                # with col1:
                #     st.metric("Original Text", f"{len(text_input)} chars")
                # with col2:
                #     st.metric("Summary", f"{len(summary)} chars")
                
                st.markdown("---")
                
                # Summary
                st.subheader("📄 Summary")
                st.write(summary)
                
                st.markdown("---")
                
                # Action Items and Key Decisions
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("✅ Action Items")
                    if extract_data["action_items"]:
                        for item in extract_data["action_items"]:
                            st.markdown(f"- {item}")
                    else:
                        st.info("No action items found")
                
                with col2:
                    st.subheader("🎯 Key Decisions")
                    if extract_data["key_decisions"]:
                        for decision in extract_data["key_decisions"]:
                            st.markdown(f"- {decision}")
                    else:
                        st.info("No key decisions found")
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure the API server is running on port 8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


