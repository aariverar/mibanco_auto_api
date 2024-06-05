const fs = require('fs');

// Leer el archivo JSON generado por behave
const reportJson = JSON.parse(fs.readFileSync('report.json', 'utf8'));

// Transformar la estructura del JSON para cumplir con lo esperado por cucumber-html-reporter
const transformedReport = reportJson.map(feature => {
    return {
        uri: feature.uri || 'unknown.feature',
        id: feature.id || '',
        keyword: feature.keyword || 'Feature',
        name: feature.name || '',
        description: feature.description || '',
        line: feature.line || 1,
        elements: feature.elements || [],
    };
});

// Guardar el archivo JSON transformado
fs.writeFileSync('report-transformed.json', JSON.stringify(transformedReport, null, 2));
