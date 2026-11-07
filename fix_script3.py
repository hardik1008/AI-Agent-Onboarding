tailwind_config = """    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#eef2ff',
              100: '#e0e7ff',
              200: '#c7d2fe',
              500: '#4f46e5',
              600: '#4338ca',
              700: '#3730a3',
              900: '#1e1b4b',
            },
            emerald: {
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
            }
          }
        }
      }
    };"""

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\extracted_script_3.js", "w", encoding="utf-8") as f:
    f.write(tailwind_config)
print("Updated extracted_script_3.js")
