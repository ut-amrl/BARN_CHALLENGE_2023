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



#include <ATen/ops/erf_ops.h>

namespace at {


// aten::erf(Tensor self) -> Tensor
inline at::Tensor erf(const at::Tensor & self) {
    return at::_ops::erf::call(self);
}

// aten::erf_(Tensor(a!) self) -> Tensor(a!)
inline at::Tensor & erf_(at::Tensor & self) {
    return at::_ops::erf_::call(self);
}

// aten::erf.out(Tensor self, *, Tensor(a!) out) -> Tensor(a!)
inline at::Tensor & erf_out(at::Tensor & out, const at::Tensor & self) {
    return at::_ops::erf_out::call(self, out);
}

// aten::erf.out(Tensor self, *, Tensor(a!) out) -> Tensor(a!)
inline at::Tensor & erf_outf(const at::Tensor & self, at::Tensor & out) {
    return at::_ops::erf_out::call(self, out);
}

}
