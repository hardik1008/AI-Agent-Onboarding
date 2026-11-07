INDEX_PATH = r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

target = """    <div class="p-2 bg-[#182229] border-t border-slate-800 flex space-x-1.5 overflow-x-auto text-[10px]">
      <button onclick="sendUserWhatsAppReply('🚀 Start 15h Training Course')" class="bg-[#202c33] hover:bg-[#2a3942] text-emerald-400 px-2.5 py-1 rounded-full whitespace-nowrap border border-emerald-900/50">
        🚀 Start 15h Training
      </button>
      <button onclick="sendUserWhatsAppReply('🌐 Switch to हिन्दी')" class="bg-[#202c33] hover:bg-[#2a3942] text-slate-300 px-2.5 py-1 rounded-full whitespace-nowrap border border-slate-700">
        🌐 हिन्दी
      </button>
      <button onclick="sendUserWhatsAppReply('💬 Talk to Ops Team')" class="bg-[#202c33] hover:bg-[#2a3942] text-slate-300 px-2.5 py-1 rounded-full whitespace-nowrap border border-slate-700">
        💬 Talk to Ops
      </button>
    </div>"""

replacement = """    <div id="wa-quick-replies-container" class="p-2 bg-[#182229] border-t border-slate-800 flex space-x-1.5 overflow-x-auto text-[10px]">
      <button onclick="sendUserWhatsAppReply('📋 Check My KYC Status')" class="bg-[#202c33] hover:bg-[#2a3942] text-emerald-400 px-2.5 py-1 rounded-full whitespace-nowrap border border-emerald-900/50">
        📋 Check KYC Status
      </button>
      <button onclick="sendUserWhatsAppReply('📄 Required Documents FAQ')" class="bg-[#202c33] hover:bg-[#2a3942] text-slate-300 px-2.5 py-1 rounded-full whitespace-nowrap border border-slate-700">
        📄 Required Docs
      </button>
      <button onclick="sendUserWhatsAppReply('🎓 15-Hour Training Info')" class="bg-[#202c33] hover:bg-[#2a3942] text-slate-300 px-2.5 py-1 rounded-full whitespace-nowrap border border-slate-700">
        🎓 15h Training
      </button>
      <button onclick="sendUserWhatsAppReply('🌐 Switch to हिन्दी')" class="bg-[#202c33] hover:bg-[#2a3942] text-slate-300 px-2.5 py-1 rounded-full whitespace-nowrap border border-slate-700">
        🌐 हिन्दी
      </button>
      <button onclick="sendUserWhatsAppReply('💬 Talk to Ops Team')" class="bg-[#202c33] hover:bg-[#2a3942] text-slate-300 px-2.5 py-1 rounded-full whitespace-nowrap border border-slate-700">
        💬 Talk to Ops
      </button>
    </div>"""

if target in html:
    html = html.replace(target, replacement, 1)
    print("Replaced quick replies container with wa-quick-replies-container successfully!")
else:
    print("Target not found directly.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
