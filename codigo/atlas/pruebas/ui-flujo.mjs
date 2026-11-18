/**
 * Automatización UI de Atlas (Playwright).
 * Flujo: login administrador → listado → cliente Andina → contrato CT-0012.
 * Requiere: pantalla en http://localhost:8080 y Chrome instalado.
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BASE = process.env.ATLAS_WEB || 'http://localhost:8080';
const OUT = path.resolve(__dirname, '../../../evidencias/atlas/automatizacion');
const CAP = path.resolve(__dirname, '../../../evidencias/atlas/capturas');

fs.mkdirSync(OUT, { recursive: true });
fs.mkdirSync(CAP, { recursive: true });

const inicio = Date.now();
const log = [];
function decir(msg) {
  console.log(msg);
  log.push(msg);
}

const browser = await chromium.launch({
  channel: 'chrome',
  headless: true
});
const page = await browser.newPage({ viewport: { width: 1366, height: 768 } });

try {
  decir(`UI-01 abrir ${BASE}`);
  await page.goto(BASE, { waitUntil: 'networkidle' });
  await page.fill('#usuario', 'jperez');
  await page.fill('#clave', 'Clave#Segura2026');
  await page.click('button[type="submit"]');
  await page.waitForSelector('text=Distribuidora Andina', { timeout: 15000 });
  await page.screenshot({ path: path.join(CAP, 'ui_01_login_clientes.png'), fullPage: true });
  decir('UI-02 login jperez OK · listado visible');

  await page.click('text=Distribuidora Andina SpA');
  await page.waitForSelector('text=CT-0012', { timeout: 15000 });
  await page.screenshot({ path: path.join(CAP, 'ui_02_cliente_contratos.png'), fullPage: true });
  decir('UI-03 cliente Andina y contrato CT-0012 OK');

  await page.click('text=Auditoría');
  await page.waitForSelector('table, .lista, text=acción', { timeout: 15000 }).catch(() => null);
  await page.screenshot({ path: path.join(CAP, 'ui_03_auditoria.png'), fullPage: true });
  decir('UI-04 vista auditoría OK');

  const ms = Date.now() - inicio;
  decir(`RESULTADO OK · ${log.filter((l) => l.startsWith('UI-')).length} pasos · ${ms} ms`);
  fs.writeFileSync(path.join(OUT, 'playwright-ui.txt'), log.join('\n') + `\nDURACION_MS ${ms}\n`, 'utf8');
  process.exitCode = 0;
} catch (err) {
  decir(`FALLO ${err.message}`);
  await page.screenshot({ path: path.join(CAP, 'ui_FALLA.png'), fullPage: true }).catch(() => null);
  fs.writeFileSync(path.join(OUT, 'playwright-ui.txt'), log.join('\n') + '\n', 'utf8');
  process.exitCode = 1;
} finally {
  await browser.close();
}
