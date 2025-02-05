

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time

import subprocess
import os

def scrape_youtube_by_topic(topic, max_videos=100):
    try:
        # Define the question based on the topic
        question = f"What is {topic}?"

        # Create directories for storing subtitles and text files
        os.makedirs(f"data/topics/{topic}/tmp_srt", exist_ok=True)
        os.makedirs(f"data/topics/{topic}/tmp_txt", exist_ok=True)
        
        # Execute the bash command to download subtitles
        download_command = f"bash download_yt_subtitles.sh -s \"{question}\" -n {max_videos} -o data/topics/{topic}/tmp_srt"
        subprocess.run(download_command, shell=True, check=True)
        
        # Execute the bash command to convert subtitles to text
        convert_command = f"bash convert_srt_to_txt.sh data/topics/{topic}/tmp_srt data/topics/{topic}/tmp_txt"
        subprocess.run(convert_command, shell=True, check=True)

        return {"topic": topic, "status": "success"}
    
    except subprocess.CalledProcessError as e:
        # Handle errors in bash execution
        return {"topic": topic, "status": "failure", "error": str(e)}

    except Exception as e:
        # Handle any other exceptions
        return {"topic": topic, "status": "failure", "error": str(e)}


if __name__ == "__main__":
    # https://github.com/topics
    topics = ['3D', 'Ajax', 'Algorithm', 'Amp', 'Android', 'Angular', 'Ansible', 'API', 'Arduino', 'ASP.NET', 'Awesome Lists', 'Amazon Web Services', 'Azure', 'Babel', 'Bash', 'Bitcoin', 'Bootstrap', 'Bot', 'C', 'Chrome', 'Chrome extension', 'Command-line interface', 'Clojure', 'Code quality', 'Code review', 'Compiler', 'Continuous integration', 'C++', 'Cryptocurrency', 'Crystal', 'C#', 'CSS', 'Data structures', 'Data visualization', 'Database', 'Deep learning', 'Dependency management', 'Deployment', 'Django', 'Docker', 'Documentation', '.NET', 'Electron', 'Elixir', 'Emacs', 'Ember', 'Emoji', 'Emulator', 'ESLint', 'Ethereum', 'Express', 'Firebase', 'Firefox', 'Flask', 'Font', 'Framework', 'Front end', 'Game engine', 'Git', 'GitHub API', 'Go', 'Google', 'Gradle', 'GraphQL', 'Gulp', 'Hacktoberfest', 'Haskell', 'Homebrew', 'Homebridge', 'HTML', 'HTTP', 'Icon font', 'iOS', 'IPFS', 'Java', 'JavaScript', 'Jekyll', 'jQuery', 'JSON', 'The Julia Language', 'Jupyter Notebook', 'Koa', 'Kotlin', 'Kubernetes', 'Laravel', 'LaTeX', 'Library', 'Linux', 'Localization (l10n)', 'Lua', 'Machine learning', 'macOS', 'Markdown', 'Mastodon', 'Material Design', 'MATLAB', 'Maven', 'Minecraft', 'Mobile', 'Monero', 'MongoDB', 'Mongoose', 'Monitoring', 'MvvmCross', 'MySQL', 'NativeScript', 'Nim', 'Natural language processing', 'Node.js', 'NoSQL', 'npm', 'Objective-C', 'OpenGL', 'Operating system', 'P2P', 'Package manager', 'Parsing', 'Perl', 'Phaser', 'PHP', 'PICO-8', 'Pixel Art', 'PostgreSQL', 'Project management', 'Publishing', 'PWA', 'Python', 'Qt', 'R', 'Rails', 'Raspberry Pi', 'Ratchet', 'React', 'React Native', 'ReactiveUI', 'Redux', 'REST API', 'Ruby', 'Rust', 'Sass', 'Scala', 'scikit-learn', 'Software-defined networking', 'Security', 'Server', 'Serverless', 'Shell', 'Sketch', 'SpaceVim', 'Spring Boot', 'SQL', 'Storybook', 'Support', 'Swift', 'Symfony', 'Telegram', 'Tensorflow', 'Terminal', 'Terraform', 'Testing', 'Twitter', 'TypeScript', 'Ubuntu', 'Unity', 'Unreal Engine']
    max_workers = 10  # Number of workers

    results = []
    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Start the scraping tasks
        scrape_fun = lambda x: scrape_youtube_by_topic(x, max_videos=100)
        future_to_topic = {executor.submit(scrape_fun, topic): topic for topic in topics}
        
        # Use tqdm to display progress bar
        for future in tqdm(as_completed(future_to_topic), total=len(topics), desc="Scraping YouTube topics"):
            topic = future_to_topic[future]
            try:
                result = future.result()
                results.append(result)
                print(result)  # Optionally print the result
            except Exception as exc:
                print(f"{topic} generated an exception: {exc}")