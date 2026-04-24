'use client';
import GjsEditor, { Canvas } from '@grapesjs/react';
import grapesjs, { Editor } from 'grapesjs';
import 'grapesjs/dist/css/grapes.min.css';

export default function PageBuilderEditor() {
  const onEditor = (editor: Editor) => {
    // Add custom blocks for sales pages
    editor.BlockManager.add('cta-block', {
      label: 'CTA Button',
      content: `<div style="text-align:center;padding:40px;">
        <a href="#" style="background:#7b2ff7;color:#fff;padding:16px 40px;border-radius:8px;text-decoration:none;font-size:18px;font-weight:600;">
          Get Started →
        </a>
      </div>`,
      category: 'Sales',
    });

    editor.BlockManager.add('pricing-table', {
      label: 'Pricing Table',
      content: `<div style="display:flex;gap:20px;justify-content:center;padding:40px;flex-wrap:wrap;">
        <div style="border:1px solid #e0e0e0;border-radius:12px;padding:30px;text-align:center;min-width:250px;">
          <h3 style="margin:0 0 10px;">Starter</h3>
          <div style="font-size:36px;font-weight:700;margin:10px 0;">$29<span style="font-size:14px;color:#888;">/mo</span></div>
          <ul style="list-style:none;padding:0;margin:20px 0;text-align:left;">
            <li style="padding:8px 0;border-bottom:1px solid #f0f0f0;">✓ 1,000 leads/month</li>
            <li style="padding:8px 0;border-bottom:1px solid #f0f0f0;">✓ Email outreach</li>
            <li style="padding:8px 0;">✓ Basic analytics</li>
          </ul>
          <a href="#" style="display:block;background:#7b2ff7;color:#fff;padding:12px;border-radius:8px;text-decoration:none;">Choose Plan</a>
        </div>
      </div>`,
      category: 'Sales',
    });

    editor.BlockManager.add('testimonial', {
      label: 'Testimonial',
      content: `<div style="background:#f8f9fa;border-radius:12px;padding:30px;max-width:600px;margin:20px auto;">
        <p style="font-style:italic;font-size:16px;line-height:1.6;color:#333;">"This platform transformed our overseas sales process. We went from 0 to 50 clients in 3 months."</p>
        <div style="margin-top:16px;display:flex;align-items:center;gap:12px;">
          <div style="width:48px;height:48px;border-radius:50%;background:#7b2ff7;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;">JD</div>
          <div><strong>John Doe</strong><br><span style="color:#888;font-size:14px;">CEO, Acme Corp</span></div>
        </div>
      </div>`,
      category: 'Sales',
    });
  };

  return (
    <GjsEditor
      grapesjs={grapesjs}
      grapesjsCss="https://unpkg.com/grapesjs/dist/css/grapes.min.css"
      options={{
        height: '100vh',
        storageManager: false,
      }}
      plugins={['grapesjs-preset-webpage', 'grapesjs-blocks-basic']}
      onEditor={onEditor}
    >
      <Canvas />
    </GjsEditor>
  );
}
