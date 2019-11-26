# Learn Languages with AWS AI/ML

### This is a Builders Fair project for re:Invent 2019

![main image](https://github.com/noenemy/reinvent2019-buildersfair/blob/master/Buildersfair-Web/src/assets/images/background/bg-main-02.jpg)

## 1. Project Overview
A casual game to learn languages with AWS AI/ML

## 2. Project Abstract
Boost your language learning with AWS AI/ML services. This project is a casual game where you can learn multilingual fun, and users are going to take a risk adventure around the world. AWS AI / ML services are going to be the perfect technologies to help users read, write, and speak foreign languages.

## 3. Attendee Experience
The project will provide various type of education method for users to learn new languages, including picking a card with picture of the word with given time, a card with the word with given picture and pronouncing the words in right ways. This will be used for kids to learn a their mother languages and also for people who want to learn foreign languages.
 
The demo leverages Amazon Rekognition, Amazon Transcribe, Amazon Textract, Amazon Polly, Amazon RDS, Amazon ElastiCache and so on.

## 4. Development Environment Setup (macOS)

### 4.1 Prerequisites
1. Install .NET Core SDK 
   - www.microsoft.com/net/download/macos
2. Install Node and NPM
   - https://nodejs.org/en
   - Select the LTS build (recommneded for most users)
3. Install Visual Studio Code
   - https://code.visualstudio.com
4. Install Angular CLI
   - Npm install -g @angular/cli@8.3.8
5. Install Git
   - https://git-scm.com/download/mac
6. Install libgdiplus for using Graphics in API project
   - brew install mono-libgdiplus
7. Install Redis
   - brew install redis
   - redis-server (This will start the redis daemon on localhost)
8. Install Postman (optional)
   - http://www.getpostman.com
9. Recommended extensions for Visual Studio Code (optional)
   - C# by OmniSharp
   - C# Extensions
   - NuGet package manager
   - Angular v6 snippets
   - Angular files
   - Angular2-switcher
   - Angular Language service
   - Auto rename tag
   - Bracket pair colorizer
   - Debugger for Chrome
   - Material Icon Theme
   - Path Intellisense
   - Prettier
   - TSLint
  
### 4.2 How to build

1. Open a terminal
2. Move to your project folder
   - cd reinvent2018-got-talent
3. For API project (.Net core)
   - cd LifeofRoot-API
   - dotnet run (or dotnet watch run)
   - Kestrel server will run on http://localhost:5000
4. For Web project (AngularJS)
   - cd LifeofRoot-Web
   - npm update (only requires the first time for downloading app-modules)
   - ng serve
   - The website will run on http://localhost:4200
   
