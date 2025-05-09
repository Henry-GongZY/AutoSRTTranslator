# AutoSRTTranslator

一个基于Google Translate API的SRT字幕文件自动翻译工具。

## 功能特点

- 支持SRT格式字幕文件的解析和翻译
- 使用Google Cloud Translation API进行高质量翻译
- 保持原始字幕的时间轴和格式
- 支持多种目标语言的翻译

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/AutoSRTTranslator.git
cd AutoSRTTranslator
```

2. 安装依赖包：
```bash
pip install -r requirements.txt
```

3. 配置Google Cloud API密钥：
   - 在Google Cloud Console创建项目并启用Cloud Translation API
   - 获取API密钥
   - 在代码中替换`YOUR_GOOGLE_CLOUD_API_KEY`为你的实际API密钥

## 使用方法

1. 准备待翻译的SRT文件
2. 修改`srt_translator.py`中的配置：
```python
translator = SRTTranslator(api_key='YOUR_GOOGLE_CLOUD_API_KEY')
translator.translate_srt(
    input_file='input.srt',
    output_file='output.srt',
    target_language='zh'  # 目标语言代码
)
```

3. 运行翻译程序：
```bash
python srt_translator.py
```

## 支持的语言

支持Google Cloud Translation API支持的所有语言，常用的语言代码包括：
- 中文：'zh'
- 英语：'en'
- 日语：'ja'
- 韩语：'ko'
- 法语：'fr'
- 德语：'de'

## 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个项目！