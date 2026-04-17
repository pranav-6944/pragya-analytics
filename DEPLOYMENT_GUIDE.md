# Step-by-Step GitHub & Deployment Guide

## Phase 1: Uploading to GitHub

To upload this project to GitHub without uploading thousands of unnecessary files (like the `venv` or `node_modules`), I have already created a `.gitignore` file and a `requirements.txt` file for you in the root directory.

Follow these steps via your Command Prompt or VS Code terminal:

1. **Open your terminal** in the `university Analytics` folder.
2. Initialize Git:
   ```bash
   git init
   ```
3. Add all your files (the `.gitignore` will automatically skip the heavy environment folders):
   ```bash
   git add .
   ```
4. Commit your code:
   ```bash
   git commit -m "First commit: Initializing PRAGYA Analytics System"
   ```
5. Go to [github.com](https://github.com) and click **New Repository**. Give it a name (e.g., `pragya-analytics`).
6. Copy the commands GitHub gives you under *"…or push an existing repository from the command line"*. It will look like this:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/pragya-analytics.git
   git push -u origin main
   ```

---

## Phase 2: Deploying the Application

> 🛑 **CRITICAL WARNING ABOUT VERCEL:** 
> Vercel is built for frontend websites (like your React frontend). Vercel uses "Serverless Functions" for Python backends. **Your backend uses heavy libraries (`pandas`, `scikit-learn`) and takes 10+ seconds to read Excel files and train Artificial Intelligence models.** 
> Vercel limits Serverless Functions to 250MB and has a strict 10-second timeout limit on their free tier. **Vercel will crash trying to boot your AI backend.**

### The Best Alternative: Deploy to "Render" (It is better for AI)
Render.com gives you a free "Web Service" which operates like a real computer, allowing your AI models to load properly and serve the React dashboard perfectly seamlessly.

**Step 1:** Go to [Render.com](https://render.com) and sign up with GitHub.
**Step 2:** Click **New +** and select **Web Service**.
**Step 3:** Connect your new GitHub repository (`pragya-analytics`).
**Step 4:** Configure the settings exactly as follows:
* **Name:** Pragya-Analytics
* **Language:** Python 3
* **Root Directory:** (leave blank)
* **Build Command:** 
  ```bash
  pip install -r requirements.txt && cd Bonus_FastAPI/frontend && npm install && npm run build
  ```
* **Start Command:** 
  ```bash
  cd Bonus_FastAPI && python main.py
  ```
* **Instance Type:** Free

**Step 5:** Click **Create Web Service**.

Wait roughly 5-10 minutes for Render to deploy your application. Once finished, they will give you a live URL (e.g., `https://pragya-analytics.onrender.com`), and your entire system (AI Backend + React Frontend) will be live on the internet!
