const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");
const outputName = process.env.OUTPUT_FILE;
const inputDir = process.env.INPUT_DIR_NAME;
const specifyContent = process.env.SPECIFY_CONTENT === 'true';

const insightsDir = path.join(__dirname, inputDir);
const jsonArr = [];

function parseMetadata(dir, specifyContent) {
  try {
    const files = fs.readdirSync(dir);

    for (const file of files) {
      const filePath = path.join(dir, file);

      const fileStat = fs.statSync(filePath);

      if (fileStat.isDirectory()) {
        parseMetadata(filePath, specifyContent);
      } else if (file.endsWith(".mdx") || file.endsWith(".md")) {
        const index = fs.readFileSync(filePath, "utf8");
        const { data, content } = matter(index);
        if(specifyContent) {
          jsonArr.push({...data, content });
        } else {
          jsonArr.push(data);
        }
      }
    }
  } catch (err) {
    console.log(err);
  }
}

parseMetadata(insightsDir, specifyContent);

const content = JSON.stringify(jsonArr, null, 2);

try {
    fs.writeFileSync(`${outputName}.json`, content);
} catch(err) {
    console.log('Error writing file', err);
}