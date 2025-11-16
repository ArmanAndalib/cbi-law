import os

def get_law_text_manually():
    """
    Get law text through manual copy-paste
    """
    print("📝 PERSIAN LAW TEXT INPUT")
    print("=" * 60)
    print("Please paste the Persian law text you copied.")
    print("Press Enter twice when you're finished.")
    print("=" * 60)
    
    input("Press Enter to start pasting...")
    
    print("\n📋 Paste your text below (press Enter twice when done):")
    print("-" * 50)
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n⏹️ Input cancelled")
            return None
    
    law_text = '\n'.join(lines)
    
    if law_text.strip():
        # Save to file
        with open('persian_law.txt', 'w', encoding='utf-8') as f:
            f.write(law_text)
        
        print(f"\n✅ Success! Saved {len(law_text)} characters to 'persian_law.txt'")
        
        # Show preview
        print("\n📄 Preview:")
        print("=" * 40)
        print(law_text[:500] + "..." if len(law_text) > 500 else law_text)
        print("=" * 40)
        
        return law_text
    else:
        print("❌ No text received")
        return None

if __name__ == "__main__":
    get_law_text_manually()