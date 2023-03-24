#pragma once

// @generated by torchgen/gen.py from Operator.h

#include <tuple>
#include <vector>

// Forward declarations of any types needed in the operator signatures.
// We can't directly include these classes because it will cause circular include dependencies.
// This file is included by TensorBody.h, which defines the Tensor class.
#include <ATen/core/ATen_fwd.h>

namespace at {
namespace _ops {


struct TORCH_API cummin {
  using schema = ::std::tuple<at::Tensor,at::Tensor> (const at::Tensor &, int64_t);
  using ptr_schema = schema*;
  // See Note [static constexpr char* members for windows NVCC]
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(name, "aten::cummin")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(overload_name, "")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(schema_str, "cummin(Tensor self, int dim) -> (Tensor values, Tensor indices)")
  static ::std::tuple<at::Tensor,at::Tensor> call(const at::Tensor & self, int64_t dim);
  static ::std::tuple<at::Tensor,at::Tensor> redispatch(c10::DispatchKeySet dispatchKeySet, const at::Tensor & self, int64_t dim);
};

struct TORCH_API cummin_out {
  using schema = ::std::tuple<at::Tensor &,at::Tensor &> (const at::Tensor &, int64_t, at::Tensor &, at::Tensor &);
  using ptr_schema = schema*;
  // See Note [static constexpr char* members for windows NVCC]
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(name, "aten::cummin")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(overload_name, "out")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(schema_str, "cummin.out(Tensor self, int dim, *, Tensor(a!) values, Tensor(b!) indices) -> (Tensor(a!) values, Tensor(b!) indices)")
  static ::std::tuple<at::Tensor &,at::Tensor &> call(const at::Tensor & self, int64_t dim, at::Tensor & values, at::Tensor & indices);
  static ::std::tuple<at::Tensor &,at::Tensor &> redispatch(c10::DispatchKeySet dispatchKeySet, const at::Tensor & self, int64_t dim, at::Tensor & values, at::Tensor & indices);
};

struct TORCH_API cummin_dimname {
  using schema = ::std::tuple<at::Tensor,at::Tensor> (const at::Tensor &, at::Dimname);
  using ptr_schema = schema*;
  // See Note [static constexpr char* members for windows NVCC]
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(name, "aten::cummin")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(overload_name, "dimname")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(schema_str, "cummin.dimname(Tensor self, Dimname dim) -> (Tensor values, Tensor indices)")
  static ::std::tuple<at::Tensor,at::Tensor> call(const at::Tensor & self, at::Dimname dim);
  static ::std::tuple<at::Tensor,at::Tensor> redispatch(c10::DispatchKeySet dispatchKeySet, const at::Tensor & self, at::Dimname dim);
};

struct TORCH_API cummin_dimname_out {
  using schema = ::std::tuple<at::Tensor &,at::Tensor &> (const at::Tensor &, at::Dimname, at::Tensor &, at::Tensor &);
  using ptr_schema = schema*;
  // See Note [static constexpr char* members for windows NVCC]
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(name, "aten::cummin")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(overload_name, "dimname_out")
  STATIC_CONSTEXPR_STR_INL_EXCEPT_WIN_CUDA(schema_str, "cummin.dimname_out(Tensor self, Dimname dim, *, Tensor(a!) values, Tensor(b!) indices) -> (Tensor(a!) values, Tensor(b!) indices)")
  static ::std::tuple<at::Tensor &,at::Tensor &> call(const at::Tensor & self, at::Dimname dim, at::Tensor & values, at::Tensor & indices);
  static ::std::tuple<at::Tensor &,at::Tensor &> redispatch(c10::DispatchKeySet dispatchKeySet, const at::Tensor & self, at::Dimname dim, at::Tensor & values, at::Tensor & indices);
};

}} // namespace at::_ops
