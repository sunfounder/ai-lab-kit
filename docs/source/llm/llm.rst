.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _play_with_llm:

AIで遊ぼう（Multi-LLMs）
------------------------------------------------------------

**音声** と **AI** を追加することで、単なる動作や視覚の機能を超えた体験を実現できます。  
ここでは、Text-to-Speech（TTS）、Speech-to-Text（STT）、そして大規模言語モデル（LLMs）を活用し、Fusion HAT+ が話し、聞き取り、さらにはスマートロボットのように会話できる仕組みを探っていきます。

.. toctree:: 
    :maxdepth: 1

    python_tts_espeak_pico2wave
    python_tts_piper_openai
    python_stt_vosk
    python_llm_ollama
    python_online_llms
    python_local_chatbot
    python_ai_assistant

以下は試してみることができるサンプルプロジェクトです。これらはすべて OpenAI API を使用していますが、他の LLM API を利用することも可能です。

.. toctree:: 
    :maxdepth: 1

    python_openai_health.rst 
    python_openai_fan.rst 
    python_openai_blindfolded_game.rst 
    python_openai_morse_decoder.rst
    python_openai_lamp.rst 
    python_openai_book.rst 
    python_openai_pet.rst 
    python_openai_weather.rst
    python_openai_homewok.rst