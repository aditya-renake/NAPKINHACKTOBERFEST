"""Run every image in samples/ through the pipeline and save output/<name>.html."""
import glob
import os
import time
from core.image_processing import enhance
from engine.vision_ai import sketch_to_spec
from engine.codegen import spec_to_html


def run_pipeline():
    os.makedirs("output", exist_ok=True)
    sample_files = (
        glob.glob("samples/*.jpg")
        + glob.glob("samples/*.jpeg")
        + glob.glob("samples/*.png")
        + glob.glob("samples/*.JPG")
        + glob.glob("samples/*.PNG")
    )

    if not sample_files:
        print("No sample images found in samples/. Add sketches to samples/ to run tests.")
        return

    for path in sample_files:
        base_name = os.path.splitext(os.path.basename(path))[0]
        out_path = os.path.join("output", f"{base_name}.html")
        print(f"\n--- Processing: {path} ---")

        with open(path, "rb") as f:
            raw_bytes = f.read()

        t0 = time.time()
        enhanced_bytes = enhance(raw_bytes)
        t_enhance = time.time() - t0
        print(f"Enhance took: {t_enhance:.2f}s")

        t0 = time.time()
        spec = sketch_to_spec(enhanced_bytes)
        t_vision = time.time() - t0
        print(f"Vision spec took: {t_vision:.2f}s")
        print(f"Spec: {spec}")

        t0 = time.time()
        html = spec_to_html(spec)
        t_code = time.time() - t0
        print(f"Codegen took: {t_code:.2f}s")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved generated HTML to: {out_path}")


if __name__ == "__main__":
    run_pipeline()
