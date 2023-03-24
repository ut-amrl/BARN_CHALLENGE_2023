#pragma once

// @generated by torchgen/gen.py from Function.h

#include <ATen/Context.h>
#include <ATen/DeviceGuard.h>
#include <ATen/TensorUtils.h>
#include <ATen/TracerMode.h>
#include <ATen/core/Generator.h>
#include <ATen/core/Reduction.h>
#include <ATen/core/Tensor.h>
#include <c10/core/Scalar.h>
#include <c10/core/Storage.h>
#include <c10/core/TensorOptions.h>
#include <c10/util/Deprecated.h>
#include <c10/util/Optional.h>



#include <ATen/ops/rsub_ops.h>

namespace at {


// aten::rsub.Tensor(Tensor self, Tensor other, *, Scalar alpha=1) -> Tensor
inline at::Tensor rsub(const at::Tensor & self, const at::Tensor & other, const at::Scalar & alpha=1) {
    return at::_ops::rsub_Tensor::call(self, other, alpha);
}

// aten::rsub.Scalar(Tensor self, Scalar other, Scalar alpha=1) -> Tensor
inline at::Tensor rsub(const at::Tensor & self, const at::Scalar & other, const at::Scalar & alpha=1) {
    return at::_ops::rsub_Scalar::call(self, other, alpha);
}

// aten::rsub.Tensor_out(Tensor self, Tensor other, *, Scalar alpha=1, Tensor(a!) out) -> Tensor(a!)
inline at::Tensor & rsub_out(at::Tensor & out, const at::Tensor & self, const at::Tensor & other, const at::Scalar & alpha=1) {
    return at::_ops::rsub_Tensor_out::call(self, other, alpha, out);
}

// aten::rsub.Tensor_out(Tensor self, Tensor other, *, Scalar alpha=1, Tensor(a!) out) -> Tensor(a!)
inline at::Tensor & rsub_outf(const at::Tensor & self, const at::Tensor & other, const at::Scalar & alpha, at::Tensor & out) {
    return at::_ops::rsub_Tensor_out::call(self, other, alpha, out);
}

// aten::rsub.Scalar_out(Tensor self, Scalar other, Scalar alpha=1, *, Tensor(a!) out) -> Tensor(a!)
inline at::Tensor & rsub_out(at::Tensor & out, const at::Tensor & self, const at::Scalar & other, const at::Scalar & alpha=1) {
    return at::_ops::rsub_Scalar_out::call(self, other, alpha, out);
}

// aten::rsub.Scalar_out(Tensor self, Scalar other, Scalar alpha=1, *, Tensor(a!) out) -> Tensor(a!)
inline at::Tensor & rsub_outf(const at::Tensor & self, const at::Scalar & other, const at::Scalar & alpha, at::Tensor & out) {
    return at::_ops::rsub_Scalar_out::call(self, other, alpha, out);
}

}
