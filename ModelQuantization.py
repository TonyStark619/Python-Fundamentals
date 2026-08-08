# Phase 2, Day 66: Post-Training Quantization (FP32 -> INT8)
import torch

print("--- Booting LLM Quantization Engine ---")

def quantize_fp32_to_int8(tensor_fp32):
    # 1. Find the absolute maximum value in our weight matrix
    max_val = torch.max(torch.abs(tensor_fp32))
    
    # 2. Calculate the Scale Factor for INT8 (Signed integer range: -128 to 127)
    # This maps our float range directly into the integer boundary box.
    scale = max_val / 127.0
    
    # 3. Quantize: Divide by scale and round to the nearest whole integer
    tensor_int8 = torch.clamp(torch.round(tensor_fp32 / scale), -128, 127).to(torch.int8)
    
    return tensor_int8, scale

def dequantize_int8_to_fp32(tensor_int8, scale):
    # Dequantization: Multiply back by the scale factor during inference 
    # to approximate the original floating-point calculations.
    return tensor_int8.to(torch.float32) * scale

# --- Simulation Environment ---
print("Initializing Uncompressed FP32 Neural Weights...")

# Simulating a layer of weights inside a Transformer model (normally millions of parameters)
weights_fp32 = torch.tensor([
    [ 2.54, -1.12,  0.88, 3.45],
    [-0.05,  1.99, -2.78, 0.42]
], dtype=torch.float32)

original_memory_bytes = weights_fp32.nelement() * 4 # FP32 takes 4 bytes per number
print(f"Original FP32 Memory Footprint: {original_memory_bytes} bytes")

# Execute Quantization
print("\nCompressing FP32 -> INT8...")
weights_int8, scaling_factor = quantize_fp32_to_int8(weights_fp32)

compressed_memory_bytes = weights_int8.nelement() * 1 # INT8 takes 1 byte per number
print(f"Compressed INT8 Memory Footprint: {compressed_memory_bytes} bytes")
print(f"Memory Reduction Achieved: {((original_memory_bytes - compressed_memory_bytes) / original_memory_bytes) * 100:.1f}%")

# Execute Dequantization for inference check
reconstructed_fp32 = dequantize_int8_to_fp32(weights_int8, scaling_factor)

# Measure error loss introduced by compression
mse_loss = torch.mean((weights_fp32 - reconstructed_fp32) ** 2).item()

print(f"\n--- Quantization Diagnostics ---")
print(f"Scaling Factor Applied: {scaling_factor.item():.4f}")
print(f"Quantized INT8 Matrix:\n{weights_int8}")
print(f"Reconstruction Mean Squared Error (Loss): {mse_loss:.6f}")
print("\nStatus: Model compressed successfully. Ready for edge-device deployment.")